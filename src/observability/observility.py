import json, logging, time

from contextvars import ContextVar
from pathlib import Path
from functools import wraps
from uuid import uuid4
from datapizza.core.clients.models import ClientResponse
from datapizza.tracing import ContextTracing
from observability.model import AgentRunRecord, LastUsage, TokenSummary, ToolCallRecord, ToolType
from observability.pricing import compute_cost, get_default_model


_logger = logging.getLogger(__name__)


# --- Flush paths ---
_TOOL_CALLS_PATH = Path(__file__).parent / "json" / "tool_calls.json"
_AGENT_RUNS_PATH = Path(__file__).parent / "json" / "agent_runs.json"

_TRACE_LOG: list[ToolCallRecord] = []
_AGENT_LOG: list[AgentRunRecord] = []

# --- Current agent run_id (set by observe_agent, read by observe_tool) ---
_current_run_id: ContextVar[str | None] = ContextVar("_current_run_id", default=None)

# --- Last LLM usage (populated by observe_token_usage inside each LLM impl) ---
_LAST_USAGE = LastUsage()


def get_trace_log() -> list[ToolCallRecord]:
    global _TRACE_LOG
    if not _TRACE_LOG:
        _TRACE_LOG = _load_trace_log()
    return _TRACE_LOG


def get_agent_log() -> list[AgentRunRecord]:
    global _AGENT_LOG
    if not _AGENT_LOG:
        _AGENT_LOG = _load_agent_log()
    return _AGENT_LOG


def observe_event(fn):
    """Lightweight decorator. Logs call name, latency, and ok/ko — no persistence."""
    name = fn.__name__

    @wraps(fn)
    def wrapped(*args, **kwargs):
        t0 = time.time()
        ok = True
        try:
            out = fn(*args, **kwargs)
            return out
        except Exception:
            ok = False
            raise
        finally:
            dt = round((time.time() - t0) * 1000, 1)
            status = "ok" if ok else "error"
            _logger.info(f"[{status}] {name} — {dt}ms")

    return wrapped


def observe_tool_run(tool_type: ToolType):
    """Decorator factory. Wraps an impl function with ContextTracing span, latency
    measurement, token/cost capture (LLM only), and TRACE_LOG append + flush."""
    def decorator(fn):
        name = fn.__name__
       
        _logger.info(f"Decorating tool '{name}' with observability (type={tool_type}).")
        
        @wraps(fn)
        def wrapped(*args, **kwargs):
            _LAST_USAGE.model = None
            _LAST_USAGE.prompt_tokens = 0
            _LAST_USAGE.completion_tokens = 0

            t0 = time.time()
            ok = True
            try:
                with ContextTracing().trace(f"tool.{name}"):
                    out = fn(*args, **kwargs)
            except Exception as e:
                out = json.dumps({"error": str(e)})
                ok = False
            dt = (time.time() - t0) * 1000

            if tool_type in (ToolType.LOCAL_LLM, ToolType.REMOTE_LLM):
                model = _LAST_USAGE.model or get_default_model()
                ptok = _LAST_USAGE.prompt_tokens
                ctok = _LAST_USAGE.completion_tokens
                cost = compute_cost(ptok, ctok, model)
                
                _logger.info(f"Observed tool run for LLM '{model}': prompt={ptok}, completion={ctok}, cost={cost:.6f} EUR")
            else:
                model, ptok, ctok, cost = None, 0, 0, 0.0

            _TRACE_LOG.append(ToolCallRecord(
                run_id=_current_run_id.get(),
                toolName=name,
                type=tool_type,
                latency_ms=round(dt, 1),
                ok=ok,
                llm_model=model,
                input_tokens=ptok,
                output_tokens=ctok,
                cost_eur=round(cost, 6),
                ts=time.time(),
            ))
            _flush_trace_log()
            return out

        return wrapped
    return decorator


def observe_agent_run(fn):
    """Decorator. Wraps an agent run with run_id context, latency, token aggregation, and AGENT_LOG append."""
    name = fn.__name__

    @wraps(fn)
    def wrapped(*args, **kwargs):
        run_id = str(uuid4())
        token = _current_run_id.set(run_id)

        _LAST_USAGE.model = None
        _LAST_USAGE.prompt_tokens = 0
        _LAST_USAGE.completion_tokens = 0

        t0 = time.time()
        ok = True
        try:
            with ContextTracing().trace(f"agent.{name}"):
                out = fn(*args, **kwargs)
        except Exception as e:
            out = json.dumps({"error": str(e)})
            ok = False
        finally:
            _current_run_id.reset(token)

        dt = (time.time() - t0) * 1000

        # Agent's own LLM tokens (set by observe_token_usage called inside devagent)
        agent_model = _LAST_USAGE.model or get_default_model()
        a_ptok = _LAST_USAGE.prompt_tokens
        a_ctok = _LAST_USAGE.completion_tokens
        a_cost = compute_cost(a_ptok, a_ctok, agent_model)

        # Tool tokens: aggregate all tool records produced during this run
        run_tool_records = [r for r in _TRACE_LOG if r.run_id == run_id]
        t_ptok = sum(r.input_tokens for r in run_tool_records)
        t_ctok = sum(r.output_tokens for r in run_tool_records)
        t_cost = sum(r.cost_eur for r in run_tool_records)

        _AGENT_LOG.append(AgentRunRecord(
            run_id=run_id,
            agentName=name,
            latency_ms=round(dt, 1),
            ok=ok,
            llm_model=agent_model if _LAST_USAGE.model else None,
            agent_tokens=TokenSummary(input=a_ptok, output=a_ctok, cost_eur=round(a_cost, 6)),
            tool_tokens=TokenSummary(input=t_ptok, output=t_ctok, cost_eur=round(t_cost, 6)),
            total_tokens=TokenSummary(
                input=a_ptok + t_ptok,
                output=a_ctok + t_ctok,
                cost_eur=round(a_cost + t_cost, 6),
            ),
            tool_calls_names=[r.toolName for r in run_tool_records],
            ts=time.time(),
        ))
        _flush_trace_log()
        return out

    return wrapped


def observe_token_usage(response: ClientResponse, model: str) -> None:
    """Call inside an LLM impl right after client.structured_response/invoke to capture token usage."""
    _LAST_USAGE.model = model
    _LAST_USAGE.prompt_tokens = response.usage.prompt_tokens
    _LAST_USAGE.completion_tokens = response.usage.completion_tokens
    
    _logger.info(f"Observed token usage for model '{model}': prompt={response.usage.prompt_tokens}, completion={response.usage.completion_tokens}")   


def _load_trace_log() -> list[ToolCallRecord]:
    if _TOOL_CALLS_PATH.exists() and _TOOL_CALLS_PATH.stat().st_size > 0:
        return [ToolCallRecord(**r) for r in json.loads(_TOOL_CALLS_PATH.read_text(encoding="utf-8"))]
    return []


def _load_agent_log() -> list[AgentRunRecord]:
    if _AGENT_RUNS_PATH.exists() and _AGENT_RUNS_PATH.stat().st_size > 0:
        return [AgentRunRecord(**r) for r in json.loads(_AGENT_RUNS_PATH.read_text(encoding="utf-8"))]
    return []


def _flush_trace_log() -> None:
    """Flush TRACE_LOG → tool_calls.json and AGENT_LOG → agent_runs.json."""
    _TOOL_CALLS_PATH.write_text(
        json.dumps([r.model_dump(mode="json") for r in _TRACE_LOG], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    _AGENT_RUNS_PATH.write_text(
        json.dumps([r.model_dump(mode="json") for r in _AGENT_LOG], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    _logger.info(
        f"Flushed {len(_AGENT_LOG)} agent runs to {_AGENT_RUNS_PATH.name}, "
        f"{len(_TRACE_LOG)} tool calls to {_TOOL_CALLS_PATH.name}."
    )
