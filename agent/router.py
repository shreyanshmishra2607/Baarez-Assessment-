import re
from tools.calculator import tool_calculate
from tools.memory import tool_save_memory, tool_get_memory

# Tool registry
TOOLS = {
    "calculator": tool_calculate,
    "memory_save": tool_save_memory,
    "memory_read": tool_get_memory
}


def agent_router(prompt: str) -> dict:
    text = prompt.lower().strip()

    # ---------- MEMORY SAVE ----------
    save_match = re.search(r"(remember|save) (.+) is (.+)", text)

    if save_match:
        key = save_match.group(2).replace("my ", "").strip()
        value = save_match.group(3).strip()

        response = TOOLS["memory_save"](key, value)

        return {
            "chosen_tool": "memory_save",
            "tool_input": f"{key} -> {value}",
            "confidence": 0.95,
            "response": response
        }

    # ---------- MEMORY READ ----------
    read_match = re.search(r"(what is my|recall) (.+)", text)

    if read_match:
        key = read_match.group(2).replace("my ", "").replace("?", "").strip()


        response = TOOLS["memory_read"](key)

        return {
            "chosen_tool": "memory_read",
            "tool_input": key,
            "confidence": 0.90,
            "response": response
        }

    # ---------- CALCULATOR ----------
    if "what is" in text or "calculate" in text:

        expression = (
            text.replace("what is", "")
                .replace("calculate", "")
                .replace("plus", "+")
                .replace("minus", "-")
                .replace("times", "*")
                .replace("multiplied by", "*")
                .replace("divided by", "/")
                .replace("?", "")
                .strip()
        )

        response = TOOLS["calculator"](expression)

        return {
            "chosen_tool": "calculator",
            "tool_input": expression,
            "confidence": 0.88,
            "response": response
        }

    # ---------- FALLBACK ----------
    return {
        "error": "I do not have a tool for that.",
        "confidence": 0.0
    }
