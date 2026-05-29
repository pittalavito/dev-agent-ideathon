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
        st.write(run_dev_agent(api_doc))

    st.divider()
    render_logs()
        
        
