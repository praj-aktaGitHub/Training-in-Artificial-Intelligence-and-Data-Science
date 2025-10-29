import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")


llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
notes = []

@tool
def summarize(text: str) -> str:
    """Summarize the convo."""
    prompt = f"Summarize the convo"
    return llm.invoke(prompt).content

@tool
def analyze(text: str) -> str:
    """Analyze the vibe"""
    prompt = f"Analyze the vibe"
    return llm.invoke(prompt).content

@tool
def note(text: str) -> str:
    """Add notes to the vibe"""
    notes.append(text)
    return f'Noted: "{text.strip()}"'

@tool
def get_note(dummy: str) -> str:
    """Retrive stored notes"""
    if not notes:
        return "you have no notes."
    return f"You currently have {len(notes)} note(s): " + "; ".join(f'"{n}"' for n in notes)

@tool
def improve(text: str) -> str:
    """Improve the vibe"""
    prompt = f"Improve the vibe"
    return llm.invoke(prompt).content

@tool
def priority(task: str) -> str:
    """Classify task as priority"""
    prompt = f"Classify task as priority"
    return llm.invoke(prompt).content

tools = [summarize, analyze, note, get_note, improve, priority]

agent = initialize_agent(
    tools = tools,
    llm = llm,
    agent = AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory = memory,
    verbose = False,
    handle_parsing_errors=True
)

print("\n=== AI Productivity Assistant ===")
print("Type 'bye' to quit.")
while True:
    user_input = input("User: ").strip()
    if user_input == "bye":
        print("\nSee ya later!")
        break

    try:
        response = agent.run(user_input)
        print("Agent:", response)
    except Exception as e:
        print("Agent: Something went wrong:", str(e))

