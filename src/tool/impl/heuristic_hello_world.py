from tool.contract import HelloWordContract

def heuristic_hello_world(name: str) -> str:
    """Heuristic: This tool takes a name as input and returns a greeting message."""
    hello_word = HelloWordContract(response=f"Hello, {name}!")
    response = hello_word.model_dump_json(indent=2)    
    return response