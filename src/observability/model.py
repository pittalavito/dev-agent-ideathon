from enum import Enum
from pydantic import BaseModel

class ToolType(Enum):
    DETERMINISTIC = "deterministic"
    LLM = "llm"

class ToolCallRecord(BaseModel):
    toolName: str
    type: ToolType
    latency_ms: float = 0.0
    ok: bool = True
    llm_model: str = None
    input_tokens: int = 0
    output_tokens: int = 0
    cost_eur: float = 0.0
    ts: float = 0.0