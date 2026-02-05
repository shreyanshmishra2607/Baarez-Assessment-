from tools.calculator import tool_calculate
from tools.memory import tool_save_memory, tool_get_memory


def agent_router(prompt: str) -> dict:
    text = prompt.lower().strip()

    # ---------------- MEMORY READ ----------------
    if "what is my" in text or "recall" in text:
        key = (
            text.replace("what is my", "")
                .replace("recall", "")
                .replace("?", "")
                .strip()
        )
                    
        result = tool_get_memory(key)

        return {
            "chosen_tool": "memory_read",
            "tool_input": key,
            "response": result
        }

    # ---------------- MEMORY SAVE ----------------
    if "remember" in text or "save" in text:
        cleaned = (
            text.replace("remember", "")
                .replace("save", "")
                .strip()
        )

        if " is " in cleaned:
            key, value = cleaned.split(" is ", 1)

            key = key.replace("my ", "").strip()
            value = value.strip()

            result = tool_save_memory(key, value)

            return {
                "chosen_tool": "memory_save",
                "tool_input": f"{key} -> {value}",
                "response": result
            }

    # ---------------- CALCULATOR ----------------
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

        result = tool_calculate(expression)

        return {
            "chosen_tool": "calculator",
            "tool_input": expression,
            "response": result
        }

    # ---------------- FALLBACK ----------------
    return {
        "error": "I do not have a tool for that."
    }
