import os

from datapizza.clients.google import GoogleClient
from datapizza.clients.openai import OpenAIClient
from dotenv import load_dotenv
from observability.observility import observe_event


load_dotenv()


### CLIENT REGISTRY ###
_FAST_CLIENT: OpenAIClient = None
_LOCAL_CLIENT: OpenAIClient = None


### GETTER FOR CLIENT ###
def get_fast_client() -> OpenAIClient:
  """Singleton pattern for Fast Client."""
  return _FAST_CLIENT


def get_local_client() -> OpenAIClient:
  """Singleton pattern for Local Client."""
  return _LOCAL_CLIENT

 
### INITIALIZATION CLIENT ###
def init_clients():
  """Initialize all clients at startup. Skips if already initialized."""
  global _FAST_CLIENT, _LOCAL_CLIENT
  if _FAST_CLIENT is None:
    _FAST_CLIENT = _init_fast_client()
  if _LOCAL_CLIENT is None:
    _LOCAL_CLIENT = _init_local_client()


@observe_event
def _init_fast_client() -> OpenAIClient:
  """Initialize the fast client"""
  return OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0.1
  )


@observe_event
def _init_local_client() -> OpenAIClient:
  """Initialize the local client"""
  return OpenAIClient(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model="gemma3:4b"
  )