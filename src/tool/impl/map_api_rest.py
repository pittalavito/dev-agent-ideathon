import json

from client.client import get_fast_client
from tool.contract import ApiRestContract


def map_api_rest(text: str) -> str:
    """Receives a textual api documentation and maps it to a structured ApiRestContract."""
    
    INPUT = f"Trasforma questa documentazione API in una struttura dati: {text}"
    
    SYSTEM_PROMPT = (
        "Sei un assistente che prende una documentazione testuale di un'API REST"
        "E la trasforma in una struttura dati per effettuare una chiamata API REST."
        "La struttura dati deve essere un oggetto ApiRestContract con i seguenti campi: method, uri, request_params, path_params, request_body."
        "request_params, path_params e request_body devono essere liste di oggetti con campi name e value."
        "Se un gruppo di campi non esiste, restituisci una lista vuota."
    )
    
    client = get_fast_client()
    
    response = client.structured_response(
        input=INPUT,
        system_prompt=SYSTEM_PROMPT,
        output_cls=ApiRestContract,
        temperature=0.1
    )
    
    structured_response: ApiRestContract = response.structured_data[0]
    result = json.dumps(structured_response.model_dump(), ensure_ascii=False, indent=2)
    return result