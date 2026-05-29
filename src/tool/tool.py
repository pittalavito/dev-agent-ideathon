import json
import re
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
    
    INPUT = f"API doc:\n{text}"

    SYSTEM_PROMPT = (
        "Converti documentazione API REST in ApiRestContract JSON: "
        "method, uri, request_params, path_params, request_body, responses. "
        "request_params, path_params, request_body: lista di {name, value}. "
        "responses: lista di {status_code, description, body:[{name, type, description}]}. "
        "Lista vuota se il gruppo non esiste."
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
    template = _strip_ts_comments(template_path.read_text(encoding="utf-8"))

    INPUT = f"Contract:\n{contract_json}"

    SYSTEM_PROMPT = (
        "Genera entity.types.ts e entity.api.ts da un contratto API REST JSON. "
        "entity_name: inferito dall'URI, PascalCase. "
        "Segui ESATTAMENTE questo template:\n\n"
        f"{template}\n\n"
        "Regole: axios via apiClient, mai fetch, mai any, valida status, usa handleAxiosError."
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


def _strip_ts_comments(ts: str) -> str:
    """Remove comments and extra blank lines from TypeScript code."""
    ts = re.sub(r'/\*[\s\S]*?\*/', '', ts)
    ts = re.sub(r'//.*', '', ts)
    ts = re.sub(r'\n\s*\n+', '\n', ts)
    return ts.strip()

    
# @tool
# @observe_tool_run(ToolType.DETERMINISTIC)
# def create_file_ts_api(contract_json: str) -> str:
#     """Receives an ApiRestContract JSON and generates TypeScript files (entity.types.ts and entity.api.ts) and creates them in src/assets/Api/{entity_name}/."""

#     template_path = Path(__file__).parent.parent / "assets" / "apiTemplate.ts"
#     template = _strip_ts_comments(template_path.read_text(encoding="utf-8"))

#     INPUT = f"Contract:\n{contract_json}"

#     SYSTEM_PROMPT = (
#         "crea la cartella che descrive l'endPoint e i file entity.types.ts e entity.api.ts dalla risposta precedente."
#         "Regole: pulizia del codice, evita commenti non necessari."
#     )

#     client = get_fast_client()

#     response: ClientResponse = client.structured_response(
#         input=INPUT,
#         system_prompt=SYSTEM_PROMPT,
#         output_cls=GenerateTsApiResponse,
#         temperature=0.1
#     )

#     observe_token_usage(response, model=client.model_name)
#     structured_response: GenerateTsApiResponse = response.structured_data[0]
    
#     # Create directory structure and files
#     api_base_path = Path(__file__).parent.parent / "assets" / "Api" / structured_response.entity_name
#     api_base_path.mkdir(parents=True, exist_ok=True)
    
    # Write {entity_name}.types.ts
    types_file_path = api_base_path / f"{structured_response.entity_name}.types.ts"
    types_file_path.write_text(structured_response.types_file, encoding="utf-8")
    
    # Write {entity_name}.api.ts
    api_file_path = api_base_path / f"{structured_response.entity_name}.ts"
#     api_file_path.write_text(structured_response.api_file, encoding="utf-8")
    
#     result = json.dumps({
#         "entity_name": structured_response.entity_name,
#         "folder_path": str(api_base_path),
#         "types_file": str(types_file_path),
#         "api_file": str(api_file_path),
#         "status": "success",
#         "message": f"Files created successfully in {api_base_path}"
#     }, ensure_ascii=False, indent=2)
#     return result


# def _strip_ts_comments(ts: str) -> str:
#     """Remove comments and extra blank lines from TypeScript code."""
#     ts = re.sub(r'/\*[\s\S]*?\*/', '', ts)
#     ts = re.sub(r'//.*', '', ts)
#     ts = re.sub(r'\n\s*\n+', '\n', ts)
#     return ts.strip()


@tool
@observe_tool_run(ToolType.DETERMINISTIC)
def create_file_ts_api(entity_name: str, types_file: str, api_file: str) -> str:
    """Creates TypeScript files in src/assets/Api/{entity_name}/ from pre-generated content."""
    
    # Create directory structure and files
    api_base_path = Path(__file__).parent.parent / "assets" / "Api" / entity_name
    api_base_path.mkdir(parents=True, exist_ok=True)
    
    # Write entity.types.ts
    types_file_path = api_base_path / f"{entity_name}.types.ts"
    types_file_path.write_text(types_file, encoding="utf-8")
    
    # Write entity.api.ts
    api_file_path = api_base_path / f"{entity_name}.ts"
    api_file_path.write_text(api_file, encoding="utf-8")
    
    result = json.dumps({...})
    return result