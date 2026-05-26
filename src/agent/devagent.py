
from observability.observe import get_logger
from datapizza.agents import Agent
from datapizza.tools import Tool
from dotenv import load_dotenv
from client.client import get_fast_client
from tool.tool import heuristic_hello_world, llm_hello_world, map_api_rest

load_dotenv()


### LOGGING SETUP ###
_LOG_PREFIX = "[agent]"
_logger = get_logger()

### GLOBALS ###
_dev_agent: Agent = None


def run_dev_agent(input: str) -> str:
  """Run the Agent with the given input."""
  
  _logger.info(f"{_LOG_PREFIX}: run_dev_agent called")

  global _dev_agent
  
  if _dev_agent is None:
    init_dev_agent()
    
  response = _dev_agent.run(input)
  return response.text[:2500]


def init_dev_agent():
  """Initialize the Agent with the system prompt and tools."""  
  
  _logger.info(f"{_LOG_PREFIX}: Initializing DevAgent")
  
  global _dev_agent
  
  _dev_agent = Agent(
    name="DevAgent",
    client=get_fast_client(),
    system_prompt=_system_promt(),
    tools=[map_api_rest],
    max_steps=2,
    terminate_on_text=True,
    #output_cls=str
  )


def _system_promt() -> str:
  """System prompt for the DevAgent."""  
  
  return """Sei uno sviluppatore Software FE, stack (React, Typescript). 
  chiedi all'utente di fornirti la documentazione testuale di un API REST e mappala in un contratto strutturato ApiRestContract. 
  """