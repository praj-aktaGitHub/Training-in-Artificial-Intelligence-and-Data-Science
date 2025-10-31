import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import tool

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Set up LLM
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url
)

# Set up memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Optional tool to show memory
@tool
def show_history(dummy: str) -> str:
    """Show previous inputs and outputs."""
    messages = memory.load_memory_variables({}).get("chat_history", [])
    if not messages:
        return "No history yet."
    return "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in messages])

tools = [show_history]

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=False,
    handle_parsing_errors=True
)

# Start chat loop
print("\n=== 🧠 Context-Aware Memory Bot ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nBot: Catch you later 🧠")
        break

    try:
        response = agent.run(user_input)
        print("Bot:", response)
    except Exception as e:
        print("Bot: Something went wrong:", str(e))
