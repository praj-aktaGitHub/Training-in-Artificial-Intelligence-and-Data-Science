import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()
llm_api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Set up LLM
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=llm_api_key,
    base_url=base_url
)

# Set up memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Tool: Mood Analyzer
@tool
def analyze_mood(text: str) -> str:
    """Analyze the emotional tone of a user's message."""
    prompt = (
        "Analyze the emotional tone of the following message. "
        "Classify it as Positive, Negative, or Neutral, and explain why.\n\n"
        f"Message: {text}"
    )
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error analyzing mood: {str(e)}"

# Initialize agent with memory and tool
tools = [analyze_mood]
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=False,
    handle_parsing_errors=True
)

# Chat loop
print("\n=== 🧠 Mood Memory Bot ===")
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
