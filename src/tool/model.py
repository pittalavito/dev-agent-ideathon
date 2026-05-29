from enum import Enum
from pydantic import BaseModel, Field


class ToolType(str, Enum):
    LOCAL_LLM = "local_llm"
    REMOTE_LLM = "remote_llm"
    DETERMINISTIC = "deterministic"


### MAP API REST TOOL CONTRACTS ######################################################################################################

class ApiRestField(BaseModel):
    name: str = Field(..., description="Field name.")
    value: str = Field(..., description="Field value.")


class ApiRestMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

class ApiRestResponseField(BaseModel):
    """Un singolo campo nella response body di un'API REST."""
    name: str = Field(..., description="Field name.")
    type: str = Field(..., description="Field type (e.g., string, number, uuid, timestamp, array).")
    description: str = Field(default="", description="Brief description of the field.")

class ApiRestResponse(BaseModel):
    """Una singola response possibile (per status code)."""
    status_code: int = Field(..., description="HTTP status code (e.g., 200, 201, 400, 404).")
    description: str = Field(default="", description="Brief description of the response.")
    body: list[ApiRestResponseField] = Field(
        default_factory=list, 
        description="Response body fields. Empty list if no body."
    )
    

class MapApiRestToolResponse(BaseModel):
    method: ApiRestMethod
    uri: str
    request_params: list[ApiRestField]
    path_params: list[ApiRestField]
    request_body: list[ApiRestField]
    responses: list[ApiRestResponse] = Field(
      default_factory=list,
      description="Possible API responses, one for status code."
    )


### OTHER TOOL CONTRACTS ############################################################################################################


class GenerateTsApiResponse(BaseModel):
    entity_name: str = Field(..., description="Entity name in PascalCase (e.g., User).")
    types_file: str = Field(..., description="Full content of entity.types.ts with typed RequestDTO and ResponseDTO interfaces.")
    api_file: str = Field(..., description="Full content of entity.api.ts following the apiTemplate structure.")

