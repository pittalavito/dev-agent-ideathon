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
    # In src/tool/tool.py -> def map_api_rest(text: str):
    INPUT = f"API doc:\n{re.sub(r'\s+', ' ', text).strip() }"

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