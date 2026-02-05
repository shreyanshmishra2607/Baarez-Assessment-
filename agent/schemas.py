from pydantic import BaseModel
from typing import Any

class AgentRequest(BaseModel):
    prompt: str


class AgentResponse(BaseModel):
    original_prompt: str
    chosen_tool: str
    tool_input: str
    response: Any
