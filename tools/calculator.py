import re

def tool_calculate(expression: str) -> dict:
    # allow only numbers and operators
    if not re.match(r"^[0-9+\-*/(). ]+$", expression):
        return {"error": "Invalid expression"}

    try:
        result = eval(expression)
        return {"result": result}
    except:
        return {"error": "Calculation failed"}
