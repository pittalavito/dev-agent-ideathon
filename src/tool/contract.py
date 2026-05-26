from enum import Enum

from pydantic import BaseModel, Field

class HelloWordContract(BaseModel):
    response: str = Field(..., description="The response message.")


class ApiRestField(BaseModel):
    name: str = Field(..., description="Field name.")
    value: str = Field(..., description="Field value.")


class ApiRestMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    

class ApiRestContract(BaseModel):
    method: ApiRestMethod = Field(..., description="HTTP method (e.g., GET, POST).")
    uri: str = Field(..., description="API endpoint (e.g., /users).")
    request_params: list[ApiRestField] = Field(default_factory=list, description="Query parameters for the API request.")
    path_params: list[ApiRestField] = Field(default_factory=list, description="Path parameters for the API endpoint.")
    request_body: list[ApiRestField] = Field(default_factory=list, description="Body fields for the API request.") 





