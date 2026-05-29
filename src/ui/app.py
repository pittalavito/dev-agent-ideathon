import streamlit as st

from agent.devagent import run_dev_agent
from ui.logs_page import render_logs


def StartHomePage() -> None:
    """The home page of the Streamlit app."""
    st.set_page_config(page_title="Ideathon AI", page_icon="AI", layout="wide")
    st.title("Ideathon AI")
    st.write("UI minima in Streamlit per provare rapidamente input, stato e layout.")

    st.write("Test ApiRestAgent: Inserisci la documentazione testuale di un API REST e mappala in un contratto strutturato ApiRestContract.")
   
    st.radio("Inserisci la documentazione API REST", ("Testo Libero", "Dettagliato"), key="typeInput_selector")

    api_doc = None
    api_dettaglio = None

    if st.session_state.typeInput_selector == "Testo Libero":
        api_doc = st.text_area("Inserisci il testo libero:", key="api_doc")
    else:
        st.write("Inserisci i dettagli:")
        method = st.selectbox("Metodo", ("GET", "POST", "PUT", "DELETE"))
        uri = st.text_input("URI", key="uri_key", placeholder="/api/v1/resource")
        request_params = st.text_input("Request params", key="request_params_key", placeholder="[{name: string, value: string}, {name: string, value: string}]")
        path_params = st.text_input("Path params", key="path_params_key", placeholder="[{name: string, value: string}, {name: string, value: string}]")
        request_body = st.text_input("Request body", key="request_body_key", placeholder="[{name: string, value: string}, {name: string, value: string}]")
        responses = st.text_input("Responses", key="responses_key", placeholder="[{name: string, value: string}, {name: string, value: string}]")

        api_dettaglio = (
            f"Metodo: {method}\n"
            f"URI: {uri}\n"
            f"Request params: {request_params}\n"
            f"Path params: {path_params}\n"
            f"Request body: {request_body}\n"
            f"Responses: {responses}"
        )

    #     request_params: list[ApiRestField]
    # path_params: list[ApiRestField]
    # request_body: list[ApiRestField]

    # responses: list[ApiRestResponse] = Field(
    #   default_factory=list,
    #   description="Possible API responses, one for status code."
    # )

    
    
    api_clicked = st.button("Run ", key="api_button")

    if api_clicked:
        if api_doc:
            st.write(run_dev_agent(api_doc))
        elif api_dettaglio:
            st.write(run_dev_agent(api_dettaglio))
        else:
            st.warning("Compila il campo libero o i dettagli dell'API prima di eseguire.")

    st.divider()
    render_logs()
        
        
