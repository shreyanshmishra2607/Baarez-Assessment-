from fastapi import FastAPI

from agent.schemas import AgentRequest
from agent.router import agent_router

app = FastAPI()


@app.post("/agent/query")
def query_agent(request: AgentRequest):
    prompt = request.prompt

    result = agent_router(prompt)

    if "error" in result:
        return result

    return {
        "original_prompt": prompt,
        "chosen_tool": result["chosen_tool"],
        "tool_input": result["tool_input"],
        "response": result["response"]
    }
