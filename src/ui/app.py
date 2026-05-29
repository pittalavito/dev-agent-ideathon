import json

import streamlit as st

from agent.devagent import run_dev_agent
from ui.logs_page import render_logs


def StartHomePage() -> None:
    """The home page of the Streamlit app."""
    st.set_page_config(page_title="Ideathon AI", page_icon="AI", layout="wide")
    st.title("Ideathon AI")
    st.write("UI minima in Streamlit per provare rapidamente input, stato e layout.")

    st.write("Test ApiRestAgent: Inserisci la documentazione testuale di un API REST e mappala in un contratto strutturato ApiRestContract.")
    api_doc = st.text_area("Inserisci la documentazione API REST:", key="api_doc")
    api_clicked = st.button("Run ", key="api_button")

    if api_clicked and api_doc:
        output = run_dev_agent(api_doc)
        _render_agent_output(output)

    st.divider()
    render_logs()


def _render_agent_output(output: str) -> None:
    try:
        # extract first JSON object from agent response
        start = output.index("{")
        end = output.rindex("}") + 1
        data = json.loads(output[start:end])
    except (ValueError, json.JSONDecodeError):
        st.write(output)
        return

    if "types_file" in data and "api_file" in data:
        entity = data.get("entity_name", "entity").lower()
        st.subheader(f"{entity}.types.ts")
        st.code(data["types_file"], language="typescript")
        st.subheader(f"{entity}.api.ts")
        st.code(data["api_file"], language="typescript")
    else:
        st.write(output)
        
        
