from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    goal: str
    last_html: str
    step_history: list
    done: bool
    next_step: dict
    result: str  # final PASS/FAIL
