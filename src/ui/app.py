import streamlit as st
from tool.tool import heuristic_hello_world, llm_hello_world, map_api_rest
from agent.devagent import run_dev_agent


def homePage() -> None:
    """The home page of the Streamlit app."""
    st.set_page_config(page_title="Ideathon AI", page_icon="AI", layout="wide")
    st.title("Ideathon AI")
    st.write("UI minima in Streamlit per provare rapidamente input, stato e layout.")

    # st.write("Puoi inserire il tuo nome qui sotto e vedere la risposta del tool `heuristic_hello_world`.")
    # heuristic_name = st.text_input("Inserisci il tuo nome:", key="heuristic_name")
    # heuristic_clicked = st.button("Esegui heuristic_hello_world", key="heuristic_button")

    # if heuristic_clicked and heuristic_name:
    #     st.write(heuristic_hello_world(heuristic_name))

    # st.write("Puoi inserire il tuo nome qui sotto e vedere la risposta del tool `llm_hello_world`.")
    #llm_name = st.text_input("Inserisci il tuo nome:", key="llm_name")
    # llm_clicked = st.button("Esegui llm_hello_world", key="llm_button")

    # if llm_clicked and llm_name:
    #    st.write(llm_hello_world(llm_name))
        
    st.write("Test ApiRestAgent: Inserisci la documentazione testuale di un API REST e mappala in un contratto strutturato ApiRestContract.")
    api_doc = st.text_area("Inserisci la documentazione API REST:", key="api_doc")
    api_clicked = st.button("Run ", key="api_button")

    if api_clicked and api_doc:
        st.write(run_dev_agent(api_doc))
