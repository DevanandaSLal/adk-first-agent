"""Math tutor agent with tools, built with Google ADK."""

import ast
import operator

from google.adk.agents import Agent

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _prepare(expr: str) -> str:
    """Turn student-style math like '2x' or '3(x+1)' into Python syntax."""
    expr = expr.replace("^", "**").replace(" ", "")
    out = []
    for i, ch in enumerate(expr):
        if i > 0:
            prev = expr[i - 1]
            if (prev.isdigit() or prev in "x)") and (ch == "x" or ch == "("):
                out.append("*")
            elif prev == ")" and ch.isdigit():
                out.append("*")
        out.append(ch)
    return "".join(out)


def _evaluate(expr: str, x: float) -> float:
    """Safely evaluate a math expression in x (no eval, only + - * / ^)."""

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Name) and node.id == "x":
            return x
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](walk(node.operand))
        raise ValueError("Only numbers, x, and + - * / ^ are supported.")

    return walk(ast.parse(_prepare(expr), mode="eval"))


def _split(equation: str) -> tuple[str, str]:
    if equation.count("=") != 1:
        raise ValueError("The equation must contain exactly one '=' sign.")
    left, right = equation.lower().split("=")
    return left, right


def check_answer(equation: str, x_value: float) -> dict:
    """Checks whether a student's value of x solves an equation.

    Args:
        equation (str): An equation in x, e.g. "2x + 5 = 13".
        x_value (float): The student's proposed value for x.

    Returns:
        dict: status, is_correct, and both sides of the equation evaluated.
    """
    try:
        left, right = _split(equation)
        lhs, rhs = _evaluate(left, x_value), _evaluate(right, x_value)
        return {
            "status": "success",
            "is_correct": abs(lhs - rhs) < 1e-9,
            "left_side": lhs,
            "right_side": rhs,
        }
    except Exception as exc:
        return {"status": "error", "error_message": str(exc)}


def solve_linear_equation(equation: str) -> dict:
    """Solves a linear equation in x so the tutor can verify its guidance.

    Args:
        equation (str): A linear equation in x, e.g. "3(x - 2) = 9".

    Returns:
        dict: status and the solution for x, or an error message.
    """
    try:
        left, right = _split(equation)

        def f(x):
            return _evaluate(left, x) - _evaluate(right, x)

        b = f(0.0)
        a = f(1.0) - b
        if abs(f(2.0) - (2 * a + b)) > 1e-9:
            return {"status": "error", "error_message": "This equation is not linear in x."}
        if abs(a) < 1e-12:
            msg = "Every x is a solution." if abs(b) < 1e-12 else "There is no solution."
            return {"status": "success", "solution": None, "note": msg}
        x = -b / a
        return {"status": "success", "solution": round(x, 6)}
    except Exception as exc:
        return {"status": "error", "error_message": str(exc)}


root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="math_tutor_agent",
    description="Helps students learn algebra by guiding them through problem-solving steps.",
    instruction="""You are a patient and encouraging algebra tutor.

Your teaching approach:
1. First understand what the student is struggling with.
2. Break the problem into small, manageable steps.
3. Guide the student to discover the answer instead of giving it directly.
4. Praise effort and progress. Use simple language and avoid jargon.

Tools:
- Use solve_linear_equation privately to know the correct answer before you guide
  the student. Do not reveal the answer unless the student asks for it or has
  tried at least twice.
- When the student proposes a value for x, ALWAYS call check_answer to verify it,
  then tell them whether they are right and why (show both sides of the equation).

Only help with math. If asked about anything else, politely steer back to math.""",
    tools=[solve_linear_equation, check_answer],
)
