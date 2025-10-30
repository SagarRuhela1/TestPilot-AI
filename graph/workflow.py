from langgraph.graph import StateGraph, START
from .state import AgentState
from .nodes import llm_decide_next_step, execute_next_step, check_done

def create_workflow():
    workflow = StateGraph(AgentState)
    workflow.add_node("decide_step", llm_decide_next_step)
    workflow.add_node("execute_step", execute_next_step)
    workflow.add_edge(START, "decide_step")
    workflow.add_edge("decide_step", "execute_step")
    workflow.add_conditional_edges("execute_step", check_done)
    return workflow.compile()
