import os

from enum import Enum
from observability.observe import get_logger
from datapizza.clients.google import GoogleClient
from datapizza.clients.openai import OpenAIClient
from dotenv import load_dotenv

load_dotenv()


### LOGGING SETUP ###
_LOG_PREFIX = "[client]"
_logger = get_logger()


### CLIENT REGISTRY ###
_fast_client: GoogleClient = None
_local_client: OpenAIClient = None


### GETTER FOR CLIENT ###
def get_fast_client() -> GoogleClient:
  """Singleton pattern for Fast Client."""
  
  _logger.info(f"{_LOG_PREFIX} Requesting Fast Client instance.")
  
  global _fast_client
  if _fast_client is None:
    _fast_client = _init_fast_client()
    
  return _fast_client


def get_local_client() -> OpenAIClient:
  """Singleton pattern for Local Client."""
  _logger.info(f"{_LOG_PREFIX} Requesting Local Client instance.")
  
  global _local_client
  if _local_client is None:
    _local_client = _init_local_client()
    
  return _local_client

 
### INTIALIZATION CLIENT ###
def intialize_clients():
  """Initialize all clients at startup."""
  _logger.info(f"{_LOG_PREFIX} Initializing all clients at startup.")

  global _fast_client
  _fast_client = _init_fast_client()
  
  global _local_client
  _local_client = _init_local_client()


def _init_fast_client() -> GoogleClient:
  """Initialize the fast client"""
  
  _logger.info(f"{_LOG_PREFIX} Initializing Fast Client with Gemini API Key.")
  
  return GoogleClient(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-3.1-flash-lite",
    temperature=0.2
  )
  
  
def _init_local_client() -> OpenAIClient:
  """Initialize the local client"""  
  
  _logger.info(f"{_LOG_PREFIX} Initializing Local Client with Ollama.")
  
  return OpenAIClient(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model="gemma4"
  )