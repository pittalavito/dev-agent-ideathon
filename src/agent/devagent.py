from datapizza.agents import Agent
from client.client import get_fast_client, get_local_client
from tool.tool import map_api_rest, generate_ts_api, create_file_ts_api
from observability.observility import observe_agent_run, observe_token_usage, observe_event


_DEV_AGENT: Agent = None
_DEV_AGENT_MODEL: str = None


@observe_agent_run
def run_dev_agent(input: str) -> str:
  """Run the Agent with the given input."""
  
  global _DEV_AGENT
  if _DEV_AGENT is None:
    _init_dev_agent()
  
  response = _DEV_AGENT.run(input)
  observe_token_usage(response, model=_DEV_AGENT_MODEL)
  return response.text


def init_dev_agent():
  """Initialize the Agent at startup."""
  global _DEV_AGENT
  if _DEV_AGENT is None:
    _init_dev_agent()


@observe_event
def _init_dev_agent():
  """Initialize the Agent with the system prompt and tools. Skips if already initialized."""
  
  global _DEV_AGENT, _DEV_AGENT_MODEL

  TOOL_REGISTRY = [map_api_rest, generate_ts_api, create_file_ts_api]
  
  SYSTEM_PROMPT = (
    "Sei un dev FE (React/TypeScript). "
    "Ricevi documentazione testuale di un'API REST. "
    "Regole: 1 tool per step. "
    "Step 1: chiama map_api_rest(text=<testo utente>). "
    "Step 2: chiama generate_ts_api(contract_json=<output esatto step 1>). "
    "Step 3: chiama create_file_ts_api(contract_json=<output esatto step 2>). "
  )
    
  client = get_fast_client()
  _DEV_AGENT_MODEL = client.model_name
  _DEV_AGENT = Agent(
    name="DevAgent",
    client=client,
    system_prompt=SYSTEM_PROMPT,
    tools=TOOL_REGISTRY,
    max_steps=4,
    terminate_on_text=True
    #output_cls
  )