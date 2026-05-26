import json

from tool.contract import HelloWordContract
from client.client import get_fast_client


def llm_hello_world(name: str) -> str:
    """LLM: This tool takes a name as input and returns a greeting message using a language model."""
    
    INPUT = f"Genera un saluto per questo nome: {name}"

    SYSTEM_PROMPT = (
        "Sei un assistente che genera saluti personalizzati. "
        "Prendi un nome come input e restituisci un oggetto HelloWord con un messaggio di saluto. "
        "Il campo response deve essere esattamente 'Hello, {name}!' adattato con il nome fornito. "
        "Non aggiungere altro testo."
    )

    client = get_fast_client()
    response = client.structured_response(
        input=INPUT,
        system_prompt=SYSTEM_PROMPT,
        output_cls=HelloWordContract,
        temperature=0.0
    )
    
    structured_response: HelloWordContract = response.structured_data[0]
    result = json.dumps(structured_response.model_dump(), ensure_ascii=False, indent=2)
    
    return result