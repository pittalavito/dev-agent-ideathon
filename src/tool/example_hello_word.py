"""Example tool implementation: Hello World.
This file demonstrates how to implement a simple tool that can be used by the Agent.        
The heuristic_hello_world function is a simple deterministic implementation that generates a greeting message based on the input name. The llm_hello_world function uses a language model to generate the greeting message, showcasing how to integrate an LLM into a tool implementation.
"""
import json

from client.client import get_fast_client
from pydantic import BaseModel, Field

class HelloWordContract(BaseModel):
    response: str = Field(..., description="The response message.")


def heuristic_hello_world(name: str) -> str:
    """Heuristic: This tool takes a name as input and returns a greeting message."""
    hello_word = HelloWordContract(response=f"Hello, {name}!")
    response = hello_word.model_dump_json(indent=2)    
    return response


def llm_hello_world(name: str) -> str:
    """LLM: This tool takes a name as input and returns a greeting message using a language model."""
    
    INPUT = f"Genera un saluto per questo nome: {name}"

    SYSTEM_PROMPT = (
        "Sei un assistente che genera saluti personalizzati. "
        "Prendi un nome come input e restituisci un oggetto HelloWord con un messaggio di saluto. "
        "Il campo response deve essere esattamente 'Hello, {name}!' adattato con il nome fornito. "
        "Non aggiungere altro testo."
    )

    client = get_fast_client()
    response = client.structured_response(
        input=INPUT,
        system_prompt=SYSTEM_PROMPT,
        output_cls=HelloWordContract,
        temperature=0.0
    )
    
    structured_response: HelloWordContract = response.structured_data[0]
    result = json.dumps(structured_response.model_dump(), ensure_ascii=False, indent=2)
    
    return result