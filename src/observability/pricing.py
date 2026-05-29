import json
from pathlib import Path

_PRICING_PATH = Path(__file__).parent / "json" / "model_pricing.json"
_CONFIG = json.loads(_PRICING_PATH.read_text(encoding="utf-8"))
_DEFAULT_MODEL: str = _CONFIG.get("default_model", "default-model")
_DEFAULT_MODEL_PRICING: dict = {"input_per_1m": 0.0, "output_per_1m": 0.0}


def get_default_model() -> str:
    return _DEFAULT_MODEL


def compute_cost(prompt_tokens: int, completion_tokens: int, model: str) -> float:
    """Compute cost in EUR based on token usage and model pricing."""
    
    model_pricing = _CONFIG.get("pricing", {})
    
    p = model_pricing.get(model, _DEFAULT_MODEL_PRICING)
    return (prompt_tokens / 1_000_000.0) * p["input_per_1m"] \
         + (completion_tokens / 1_000_000.0) * p["output_per_1m"]