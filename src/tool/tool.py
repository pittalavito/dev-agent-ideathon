import json


from datapizza.tools import tool
from observability.observe import get_logger
from tool.impl.heuristic_hello_world import heuristic_hello_world as heuristic_hello_world_tool
from tool.impl.llm_hello_world import llm_hello_world as llm_hello_world_tool
from tool.impl.map_api_rest import map_api_rest as map_api_rest_tool


### LOGGING SETUP ###
_HEURISTIC_LOG_PREFIX = "[heuristic-tool]"
_LLM_LOG_PREFIX = "[use-llm-tool]"
_logger = get_logger()


### TOOL DEFINITIONS ###
_TOOL_DEFINITIONS = {
    "heuristic-tool": ["heuristic_hello_world"],
    "llm-tool": ["llm_hello_world", "map_api_rest"]
}


### TOOLS IMPLEMENTATION ###
@tool
def heuristic_hello_world(name: str) -> str:
    """Heuristic: This tool takes a name as input and returns a greeting message."""
    _logger.info(f"{_HEURISTIC_LOG_PREFIX} [heuristic_hello_world] Received input")
    
    response = heuristic_hello_world_tool(name)
    
    _logger.info(f"{_HEURISTIC_LOG_PREFIX} [heuristic_hello_world] generated response")    
    return response


@tool
def llm_hello_world(name: str) -> str:
    """LLM: This tool takes a name as input and returns a greeting message using a language model."""
    _logger.info(f"{_LLM_LOG_PREFIX} [llm_hello_world] Received input")
    
    response = llm_hello_world_tool(name)
    
    _logger.info(f"{_LLM_LOG_PREFIX} [llm_hello_world] generated response")
    return response


@tool
def map_api_rest(text: str) -> str:
    """This tool maps a textual API documentation to a structured ApiRestContract."""
    _logger.info(f"{_LLM_LOG_PREFIX} [map_api_rest] Received text input for API mapping")
       
    response = map_api_rest_tool(text)
    
    _logger.info(f"{_LLM_LOG_PREFIX} [map_api_rest] generated response")
    return response
    