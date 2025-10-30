import asyncio
from graph.workflow import create_workflow
from graph.state import AgentState

async def main():
    goal = "Go to soucedemo.com and login in with standard_user/secret_sauce"

    initial_state = AgentState(
        messages=[],
        goal=goal,
        last_html="",
        step_history=[],
        done=False,
        next_step={},
        result="IN_PROGRESS",
    )

    print("\n🚀 Starting LangGraph MCP Test Agent...\n")

    app = create_workflow()
    async for state in app.astream(initial_state):
        if state.get("done"):
            break

if __name__ == "__main__":
    asyncio.run(main())
