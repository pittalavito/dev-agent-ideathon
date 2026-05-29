import json
from pathlib import Path

from datapizza.core.clients.models import ClientResponse
from datapizza.tools import tool
from tool.model import ToolType, MapApiRestToolResponse, GenerateTsApiResponse
from client.client import get_fast_client
from observability.observility import observe_tool_run, observe_token_usage


@tool
@observe_tool_run(ToolType.REMOTE_LLM)
def map_api_rest(text: str) -> str:
    """Receives a textual api documentation and maps it to a structured ApiRestContract."""
    
    INPUT = f"Trasforma questa documentazione API in una struttura dati: {text}"
    
    SYSTEM_PROMPT = (
    "Sei un assistente che prende una documentazione testuale di un'API REST"
    "E la trasforma in una struttura dati per effettuare una chiamata API REST."
    "La struttura dati deve essere un oggetto ApiRestContract con i seguenti campi: "
    "method, uri, request_params, path_params, request_body."
    "method, uri, request_params, path_params, request_body, responses."
    "request_params, path_params e request_body devono essere liste di oggetti con campi name e value."
    "Se un gruppo di campi non esiste, restituisci una lista vuota."
    "responses deve essere una lista di oggetti, uno per ogni status code documentato. "
    "Ogni oggetto ha: status_code (intero), description (stringa breve) e body (lista di campi con name, type e description). "
    "Se la response non ha body (es. errori con solo un messaggio), metti body come lista vuota."
    )

    
    client = get_fast_client()
    
    response: ClientResponse = client.structured_response(
        input=INPUT,
        system_prompt=SYSTEM_PROMPT,
        output_cls=MapApiRestToolResponse,
        temperature=0.1
    )
    
    observe_token_usage(response, model=client.model_name)
    structured_response: MapApiRestToolResponse = response.structured_data[0]
    result = json.dumps(structured_response.model_dump(), ensure_ascii=False, indent=2)
    return result


@tool
@observe_tool_run(ToolType.REMOTE_LLM)
def generate_ts_api(contract_json: str) -> str:
    """Receives an ApiRestContract JSON and generates TypeScript files (entity.types.ts and entity.api.ts)."""

    template_path = Path(__file__).parent.parent / "assets" / "apiTemplate.ts"
    template = template_path.read_text(encoding="utf-8")

    INPUT = f"Genera i file TypeScript per questo contratto API REST:\n\n{contract_json}"

    SYSTEM_PROMPT = (
        "Sei un esperto sviluppatore TypeScript React. "
        "Ricevi un contratto API REST in formato JSON con i campi: method, uri, request_params, path_params, request_body. "
        "Devi generare due file TypeScript seguendo ESATTAMENTE il template fornito:\n\n"
        f"{template}\n\n"
        "Regole:\n"
        "- entity_name: nome dell'entità inferito dall'URI (es. /users -> User), in PascalCase\n"
        "- types_file: contenuto completo di entity.types.ts con interfacce RequestDTO e ResponseDTO tipizzate dai campi del contratto\n"
        "- api_file: contenuto completo di entity.api.ts con hook useEntityAPI seguendo il template\n"
        "- Usa SOLO axios via apiClient, mai fetch\n"
        "- Rispetta tutti i forbidden patterns del template"
    )

    client = get_fast_client()

    response: ClientResponse = client.structured_response(
        input=INPUT,
        system_prompt=SYSTEM_PROMPT,
        output_cls=GenerateTsApiResponse,
        temperature=0.1
    )

    observe_token_usage(response, model=client.model_name)
    structured_response: GenerateTsApiResponse = response.structured_data[0]
    result = json.dumps(structured_response.model_dump(), ensure_ascii=False, indent=2)
    return result