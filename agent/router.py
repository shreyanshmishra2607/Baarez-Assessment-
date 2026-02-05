import re
from difflib import get_close_matches

from tools.calculator import tool_calculate
from tools.memory import tool_save_memory, tool_get_memory, Memory, SessionLocal


# Simple synonym mapping
SYNONYMS = {
    "hometown": ["place", "city", "where i live"],
    "cat's name": ["my cat", "pet name"],
    "favorite color": ["fav color", "colour"]
}


def normalize_key(key: str) -> str:
    key = key.lower().strip()

    for main_key, variations in SYNONYMS.items():
        if key == main_key:
            return main_key

        for word in variations:
            if word in key:
                return main_key

    return key


def fuzzy_match(key: str, stored_keys: list):
    match = get_close_matches(key, stored_keys, n=1, cutoff=0.6)
    return match[0] if match else None


def get_all_keys():
    db = SessionLocal()
    keys = [row.key for row in db.query(Memory).all()]
    db.close()
    return keys


def agent_router(prompt: str) -> dict:
    text = prompt.lower().strip()

    # ---------- MEMORY SAVE ----------
    save_match = re.search(r"(remember|save) (.+) is (.+)", text)

    if save_match:
        key = save_match.group(2).replace("my ", "").strip()
        value = save_match.group(3).strip()

        key = normalize_key(key)

        response = tool_save_memory(key, value)

        return {
            "chosen_tool": "memory_save",
            "tool_input": f"{key} -> {value}",
            "response": response
        }

    # ---------- MEMORY READ ----------
    read_match = re.search(r"(what is my|recall) (.+)", text)

    if read_match:
        raw_key = read_match.group(2).replace("?", "").replace("my ", "").strip()
        key = normalize_key(raw_key)

        stored_keys = get_all_keys()

        # Try exact match first
        if key not in stored_keys and stored_keys:
            fuzzy_key = fuzzy_match(key, stored_keys)
            if fuzzy_key:
                key = fuzzy_key

        response = tool_get_memory(key)


        return {
            "chosen_tool": "memory_read",
            "tool_input": key,
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

        response = tool_calculate(expression)

        return {
            "chosen_tool": "calculator",
            "tool_input": expression,
            "response": response
        }

    # ---------- FALLBACK ----------
    return {
        "error": "I do not have a tool for that."
    }
