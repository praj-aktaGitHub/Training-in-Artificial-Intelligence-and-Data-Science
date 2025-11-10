from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from datetime import datetime, timedelta
from typing import TypedDict
import json
from llm_config import llm
from fastapi.responses import JSONResponse
app = FastAPI()

# ✅ CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Logging Middleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"🔔 Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        print(f"✅ Response status: {response.status_code}")
        return response

app.add_middleware(LoggingMiddleware)

# ✅ Swagger request model
class QueryRequest(BaseModel):
    query: str

# ✅ LangGraph schema
class BotState(TypedDict, total=False):
    query: str
    task: str
    operation: str
    a: int
    b: int
    word: str
    prompt: str
    result: str
    reversed: str
    response: str
    yesterday: str
    today: str
    tomorrow: str
    error: str

# ✅ Task classifier node
def task_classifier_node(state: BotState) -> BotState:
    query = state["query"]
    prompt = f"""You are a routing assistant. Based on the user's query, choose one task:
- "math" for arithmetic operations
- "reverse" for reversing a word
- "date" for date-related queries
- "llm" for general questions

Respond with only the task name.

Query: {query}
Task:"""
    response = llm.invoke(prompt)
    task = response.content.strip().lower()
    state["task"] = task
    return state

def extract_params_node(state: BotState) -> BotState:
    query = state["query"]
    task = state["task"]

    prompt = f"""You are a smart assistant. Extract parameters from the user's query based on the task.

Task: {task}
Query: {query}

Respond with a valid JSON object using double quotes and no trailing commas.
Use integers for numbers. Examples:
- "add 5 and 7" → {{ "operation": "add", "a": 5, "b": 7 }}
- "subtract 10 from 20" → {{ "operation": "subtract", "a": 20, "b": 10 }}
- "multiply 3 and 4" → {{ "operation": "multiply", "a": 3, "b": 4 }}
- "divide 10 by 2" → {{ "operation": "divide", "a": 10, "b": 2 }}
- For "reverse": word
- For "llm": prompt
- For "date": no fields needed

JSON:"""

    response = llm.invoke(prompt)
    print("🧠 Raw LLM response:", response.content)
    try:
        extracted = json.loads(response.content.strip())
        if isinstance(extracted, dict):
            state.update(extracted)
        else:
            state["error"] = "LLM did not return a valid JSON object"
    except Exception as e:
        print(f"❌ JSON decode error: {e}")
        state["error"] = f"Failed to extract parameters: {str(e)}"
    return state


# ✅ Task nodes
def math_node(state: BotState) -> BotState:
    op = state.get("operation")
    try:
        a = int(state.get("a") or 0)
        b = int(state.get("b") or 0)
    except Exception as e:
        return {"error": f"Invalid numbers: {e}"}

    result = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "undefined",
        "modulus": a % b if b != 0 else "undefined"
    }.get(op, "invalid operation")

    return {"result": result}

def date_node(state: BotState) -> BotState:
    today = datetime.now()
    return {
        "yesterday": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        "today": today.strftime("%Y-%m-%d"),
        "tomorrow": (today + timedelta(days=1)).strftime("%Y-%m-%d")
    }

def reverse_node(state: BotState) -> BotState:
    word = state.get("word", "")
    return {"reversed": word[::-1]}

def llm_node(state: BotState) -> BotState:
    prompt = state.get("query", "")
    response = llm.invoke(prompt)
    return {"response": response.content}

# ✅ Build LangGraph
graph = StateGraph(BotState)

graph.add_node("classify", task_classifier_node)
graph.add_node("extract", extract_params_node)
graph.add_node("math", math_node)
graph.add_node("date", date_node)
graph.add_node("reverse", reverse_node)
graph.add_node("llm", llm_node)

graph.set_entry_point("classify")
graph.add_edge("classify", "extract")

graph.add_conditional_edges("extract", lambda state: state.get("task", ""), {
    "math": "math",
    "date": "date",
    "reverse": "reverse",
    "llm": "llm"
})

graph.add_edge("math", END)
graph.add_edge("date", END)
graph.add_edge("reverse", END)
graph.add_edge("llm", END)

langgraph_app = graph.compile()

@app.post("/query")
async def handle_query(data: QueryRequest):
    query = data.query
    try:
        state = langgraph_app.invoke({"query": query})

        # Extract the final answer based on task
        task = state.get("task")
        if task == "math":
            answer = state.get("result")
        elif task == "reverse":
            answer = state.get("reversed")
        elif task == "llm":
            answer = state.get("response")
        elif task == "date":
            answer = state.get("today")
        else:
            answer = "Unknown task"

        return JSONResponse(content={"answer": answer})
    except Exception as e:
        print(f"❌ Internal error: {e}")
        return JSONResponse(content={"error": f"Internal server error: {str(e)}"}, status_code=500)
