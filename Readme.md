# 🧠 LangGraph MCP Test Agent (Gemini + Playwright)

This project is a **modular automation agent** built using:
- **Gemini** (Google Generative AI) for reasoning and step planning  
- **Playwright MCP** for real browser automation  
- **LangGraph** for orchestration between planning and execution  

The agent reads a goal (like *“Login to Facebook”*), uses Gemini to plan browser actions, and executes them in sequence through the **Playwright MCP server**.

---

## 🚀 Features
✅ LLM-driven step planning using Gemini  
✅ Real browser automation via Playwright MCP  
✅ Modular project structure (`nodes`, `state`, `workflow`, `config`, `utils`)  
✅ Fully environment-driven configuration using `.env`  
✅ Works with any MCP-compatible automation server  

---

## 🏗️ Project Structure
```
AiFinalProject/
├── main.py
├── config.py
├── graph/
│   ├── nodes.py
│   ├── state.py
│   └── workflow.py
├── utils/
│   └── helper.py
├── .env
└── README.md
```

---

## ⚙️ Prerequisites
Make sure you have:
- **Python 3.12 and 3.12+**
- **Node.js 18+**
- **Playwright MCP** installed globally or locally

---

## 🧩 Step 1: Clone and Run the Microsoft Playwright MCP

Clone and start the Playwright MCP server:

```bash
npx @playwright/mcp@latest --port 8931 --shared-browser-context
```

📝 Notes:
- You can replace `8931` with any other port you prefer.
- Keep this terminal open — the Python agent connects to this MCP server via that port.

---

## 🔑 Step 2: Create a `.env` File

In your project root, create a `.env` file and add the following:

```bash
# Google Gemini API
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL_NAME=gemini-2.5-flash

# MCP Server Configuration
MCP_PLAYWRIGHT_URL=http://localhost:8931/mcp
MCP_PLAYWRIGHT_TRANSPORT=streamable_http
```

💡 *You can change the port if you ran MCP on a different one.*

---

## 🐍 Step 3: Install Python Dependencies

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, create one with:

```bash
pip install langchain-google-genai langchain-core langchain-mcp-adapters langgraph python-dotenv
pip freeze > requirements.txt
```

---

## 🧠 Step 4: Run the Agent

With the MCP server running, start your agent:

```bash
python3 main.py
```

You should see output similar to:

```
🚀 Starting LangGraph MCP Test Agent...

🧠 LLM NEXT STEP RAW:
{
  "tool": "browser_navigate",
  "args": {"url": "https://www.facebook.com"},
  "reason": "Navigating to Facebook...",
  "done": false
}

⚙️ Executing: browser_navigate with args: {'url': 'https://www.facebook.com'}
✅ Tool 'browser_navigate' executed successfully.
```

---

## ⚡ How It Works
1. **Gemini** generates a JSON plan describing the next action:
   ```json
   {
     "tool": "browser_fill_form",
     "args": {
       "fields": [
         {"selector": "#user-name", "value": "standard_user"},
         {"selector": "#password", "value": "secret_sauce"}
       ]
     },
     "reason": "Filling login fields.",
     "done": false
   }
   ```
2. **LangGraph** sends this step to the **Playwright MCP** server.  
3. MCP executes the browser action, returns HTML, and the cycle repeats.  
4. When Gemini marks `"done": true`, the process ends.

---

## 🧩 Troubleshooting

| Issue | Cause | Fix |
|-------|--------|-----|
| `⚠️ No tool found, stopping execution.` | Gemini returned `"step"` instead of `"tool"` | Ensure latest prompt from fixed `nodes.py` |
| `❌ Missing GEMINI_API_KEY` | `.env` not configured properly | Add `GEMINI_API_KEY` in `.env` |
| `MCP connection error` | MCP not running or wrong port | Run MCP with correct `--port` or update `.env` |

---

## 🧪 Example Goal

You can change the goal in **`main.py`**:

```python
goal = "Go to facebook.com and log/signin/signup in with standard_user/secret_sauce"
```

Try experimenting with other goals like:
- `"Go to saucedemo.com and login as standard_user"`
- `"Visit twitter.com and find the login button"`

---

## 🧰 Tech Stack

| Component | Purpose |
|------------|----------|
| **LangGraph** | State-based orchestration |
| **LangChain Google GenAI** | Gemini API integration |
| **Playwright MCP** | Browser automation |
| **dotenv** | Configuration management |

---

## 🧤 License

This project is for learning and testing automation frameworks using LangGraph, Playwright MCP, and Gemini.  
Use responsibly and follow all API and site terms of service.