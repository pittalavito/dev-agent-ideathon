import logging


_logger = logging.getLogger(__name__)


def get_logger() -> logging.Logger:
    """Returns a logger instance for the application."""
    return _logger


# def observe(tool_to_observe):
#    """A decorator to observe the execution of a tool function, logging entry and exit points."""
    
#    name = tool_to_observe.name if hasattr(tool_to_observe, "name") else tool_to_observe.__name__
#    inner = tool_to_observe.fn if hasattr(tool_to_observe, "fn") else tool_to_observe
#    is_llm = name in LLM_TOOL_NAMES
    
    
#    def wrapped(*args, **kwargs):
#        _logger.info(f"Entering function: {tool_to_observe.__name__}")
#
#        _LAST_USAGE["model"] = None
#        _LAST_USAGE["prompt_tokens"] = 0
#        _LAST_USAGE["completion_tokens"] = 0
#
#        t0 = time.time()
#        try:
#            with ContextTracing().trace(f"tool.{name}"):
#                out = inner(*args, **kwargs)
#            ok = True
#        except Exception as e:
#            out = {"error": str(e)}
#            ok = False
#        dt = (time.time() - t0) * 1000
#
#        if is_llm:
#            current_model = _LAST_USAGE["model"] or DEFAULT_MODEL
#            ptok = _LAST_USAGE["prompt_tokens"]
#            ctok = _LAST_USAGE["completion_tokens"]
#            cost = compute_cost(ptok, ctok, current_model)
#
#            previous = _TOOL_MODEL_REGISTRY.get(name)
#            if previous and previous != current_model:
#                dropped = sum(1 for r in TRACE_LOG if r.get("tool") == name)
#                TRACE_LOG[:] = [r for r in TRACE_LOG if r.get("tool") != name]
#                print(f"   [info] {name}: modello cambiato "
#                      f"{previous} → {current_model}, scartati {dropped} sample")
#            _TOOL_MODEL_REGISTRY[name] = current_model
#        else:
#            current_model, ptok, ctok, cost = None, 0, 0, 0.0
#
#        TRACE_LOG.append(_migrate_record({
#            "tool": name,
#            "type": "llm" if is_llm else "deterministic",
#            "latency_ms": round(dt, 1),
#            "ok": ok,
#            "model": current_model,
#            "input_tokens": ptok,
#            "output_tokens": ctok,
#            "cost_eur": round(cost, 6),
#            "ts": time.time(),
#        }))
#        
#        _logger.info(f"Exiting function: {tool_to_observe.__name__}")
#        return out
#    
#    return wrapped
    
    