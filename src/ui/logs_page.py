from datetime import datetime

import pandas as pd
import streamlit as st

from observability.observility import get_agent_log, get_trace_log


def _fmt_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S") if ts else ""


def render_logs() -> None:
    st.subheader("Observability Logs")
    if st.button("Aggiorna", key="refresh_logs"):
        st.rerun()

    tab_agents, tab_tools = st.tabs(["Agent Runs", "Tool Calls"])

    with tab_agents:
        records = [r.model_dump() for r in get_agent_log()]
        if not records:
            st.info("Nessun agent run registrato.")
        else:
            rows = [
                {
                    "run_id": r["run_id"][:8] + "…",
                    "agent": r["agentName"],
                    "ok": "✅" if r["ok"] else "❌",
                    "latency_ms": r["latency_ms"],
                    "model": r.get("llm_model") or "—",
                    "in_tok": r["total_tokens"]["input"],
                    "out_tok": r["total_tokens"]["output"],
                    "cost_eur": r["total_tokens"]["cost_eur"],
                    "tools_called": ", ".join(r.get("tool_calls_names", [])) or "—",
                    "ts": _fmt_ts(r.get("ts", 0)),
                }
                for r in records
            ]
            st.dataframe(pd.DataFrame(rows), width='stretch')

            st.markdown("**Dettaglio JSON**")
            for r in records:
                with st.expander(f"{r['run_id'][:8]}… | {r['agentName']} | {_fmt_ts(r.get('ts', 0))}"):
                    st.json(r)

    with tab_tools:
        records = [r.model_dump() for r in get_trace_log()]
        if not records:
            st.info("Nessuna tool call registrata.")
        else:
            rows = [
                {
                    "run_id": (r.get("run_id") or "")[:8] + "…",
                    "tool": r["toolName"],
                    "type": r["type"],
                    "ok": "✅" if r["ok"] else "❌",
                    "latency_ms": r["latency_ms"],
                    "model": r.get("llm_model") or "—",
                    "in_tok": r["input_tokens"],
                    "out_tok": r["output_tokens"],
                    "cost_eur": r["cost_eur"],
                    "ts": _fmt_ts(r.get("ts", 0)),
                }
                for r in records
            ]
            st.dataframe(pd.DataFrame(rows), width='stretch')

            st.markdown("**Dettaglio JSON**")
            for r in records:
                with st.expander(f"{(r.get('run_id') or '')[:8]}… | {r['toolName']} | {_fmt_ts(r.get('ts', 0))}"):
                    st.json(r)
