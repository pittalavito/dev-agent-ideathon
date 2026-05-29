from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from tool.model import ToolType  # re-exported for consumers of this module


class LastUsage(BaseModel):
    model: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0


class ToolCallRecord(BaseModel):
    run_id: Optional[str] = None
    toolName: str
    type: str
    latency_ms: float = 0.0
    ok: bool = True
    llm_model: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0
    cost_eur: float = 0.0
    ts: float = 0.0


class TokenSummary(BaseModel):
    input: int = 0
    output: int = 0
    cost_eur: float = 0.0


class AgentRunRecord(BaseModel):
    run_id: str
    agentName: str
    latency_ms: float = 0.0
    ok: bool = True
    llm_model: Optional[str] = None
    agent_tokens: TokenSummary = Field(default_factory=TokenSummary)
    tool_tokens: TokenSummary = Field(default_factory=TokenSummary)
    total_tokens: TokenSummary = Field(default_factory=TokenSummary)
    tool_calls_names: list[str] = Field(default_factory=list)
    ts: float = 0.0