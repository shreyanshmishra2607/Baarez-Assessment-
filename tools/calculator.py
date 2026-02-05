import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv
}


def safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.value


    if isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        return OPERATORS[type(node.op)](left, right)

    raise ValueError("Invalid expression")


def tool_calculate(expression: str) -> dict:
    try:
        tree = ast.parse(expression, mode="eval")
        result = safe_eval(tree.body)
        return {"result": result}
    except:
        return {"error": "Invalid expression"}
