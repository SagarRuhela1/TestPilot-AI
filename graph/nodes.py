import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from utils.helper import safe_serialize
from config import GEMINI_MODEL_NAME, MCP_SERVERS
from langgraph.graph import END

# Node 1: LLM Decides Next Step
async def llm_decide_next_step(state):
    model = ChatGoogleGenerativeAI(model=GEMINI_MODEL_NAME, temperature=0.2)
    goal = state["goal"]
    html = state.get("last_html", "")[:2000]
    history = json.dumps(state.get("step_history", []), indent=2)

    prompt = f"""
You are an expert QA automation agent using Playwright MCP tools.
Your task: "{goal}"

You can use:
- browser_navigate → {{"url": "https://..."}}
- browser_wait_for → {{"time": 3000}}
- browser_click → {{"element": "CSS selector"}}
- browser_fill_form → {{"fields": [{{"selector": "CSS selector", "value": "text"}}]}}
- browser_extract_html → {{}}

Rules:
1. Do not repeat the same navigation step twice in a row.
2. Use valid CSS selectors (#user-name, #password, #login-button).
3. If a login form is visible, mark "done": true and explain.
4. Return only **one single step at a time** as a valid JSON object — 
   never return arrays, lists, or a "steps" field.
5. Always include a "reason" field explaining the action.
6. Return valid JSON (no markdown formatting).

Example output:
{{
  "tool": "browser_fill_form",
  "args": {{
    "fields": [
      {{"selector": "#user-name", "value": "standard_user"}},
      {{"selector": "#password", "value": "secret_sauce"}}
    ]
  }},
  "reason": "Filling the login fields.",
  "done": false
}}

Current HTML snapshot (truncated): {html}
Previous steps: {history}
"""


    try:
        response = await model.ainvoke([HumanMessage(content=prompt)])
        raw = response.content.strip().replace("```json", "").replace("```", "").strip()
        print("\n🧠 LLM NEXT STEP RAW:\n", raw)
        next_step = json.loads(raw)
    except Exception as e:
        print(f"⚠️ JSON parsing error: {e}")
        next_step = {"tool": None, "args": {}, "reason": "Invalid JSON or model error", "done": True}

    # Prevent repeat steps
    history = state.get("step_history", [])
    if history:
        last = history[-1]
        if next_step.get("tool") == last.get("tool") and next_step.get("args") == last.get("args"):
            print("🛑 Detected repeated step. Stopping loop.")
            next_step["done"] = True
            next_step["reason"] = "Repeated step detected."

    return {"next_step": next_step, "messages": state["messages"] + [AIMessage(content=str(next_step))]}



# Node 2: Execute via MCP

async def execute_next_step(state):
    next_step = state.get("next_step", {})
    tool = next_step.get("tool")
    args = next_step.get("args", {})

    if not tool:
        print("⚠️ No tool found, stopping execution.")
        return {"done": True, "result": "FAIL"}

    print(f"\n⚙️ Executing: {tool} with args: {args}")
    client = MultiServerMCPClient(MCP_SERVERS)

    try:
        async with client.session("playwright") as session:
            result = await session.call_tool(tool, arguments=args)
            print(f"✅ Tool '{tool}' executed successfully.")

            try:
                html_snapshot = await session.call_tool("browser_extract_html", arguments={})
                html_content = (
                    html_snapshot.content[0].text
                    if hasattr(html_snapshot, "content")
                    else str(html_snapshot)
                )
            except Exception as e:
                print(f"⚠️ Failed to extract HTML: {e}")
                html_content = state.get("last_html", "")

    except Exception as e:
        print(f"❌ MCP execution error: {e}")
        return {"done": True, "result": "FAIL"}

    step_entry = {
        "tool": tool,
        "args": args,
        "reason": next_step.get("reason", ""),
        "result": safe_serialize(result),
        "html_length": len(html_content),
    }

    return {
        "last_html": html_content,
        "step_history": state.get("step_history", []) + [step_entry],
        "done": bool(next_step.get("done", False)),
        "result": "PASS" if next_step.get("done", False) else state.get("result", "IN_PROGRESS"),
    }



# Node 3: Check Completion

async def check_done(state):
    if state.get("done"):
        print(f"\n🏁 Task completed: {state['next_step'].get('reason', 'No reason given')}")
        return END
    return "decide_step"
