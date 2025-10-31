import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from transformers import pipeline

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# Set pup LLM
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url
)

# Set up memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

@tool
def analyze_mood(text: str) -> str:
    """Analyze user's emotional tone."""
    result = sentiment_pipeline(text)[0]
    label = result['label']
    score = result['score']
    return f"Mood: {label} ({score:.2f})"

@tool
def suggest_meditation(text: str) -> str:
    """Suggest a meditation based on mood."""
    if "anxious" in text.lower() or "stressed" in text.lower():
        return "Try box breathing: inhale 4s, hold 4s, exhale 4s, hold 4s."
    elif "tired" in text.lower():
        return "Do a body scan meditation to relax your muscles."
    return "Try a 5-minute mindfulness meditation to stay grounded."

@tool
def journaling_prompt(text: str) -> str:
    """Give a journaling prompt."""
    return "Write about one thing you're grateful for today."

@tool
def send_affirmation(text: str) -> str:
    """Send a motivational affirmation."""
    return "You are strong, capable, and resilient. 🌟 Keep going!"

@tool
def show_history(dummy: str) -> str:
    """Show previous inputs and outputs."""
    messages = memory.load_memory_variables({}).get("chat_history", [])
    if not messages:
        return "No history yet."
    return "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in messages])

tools = [analyze_mood, suggest_meditation, journaling_prompt, send_affirmation, show_history]

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=False,
    handle_parsing_errors=True
)

# Start conversation
print("\n=== 🧠 Mental Fitness Coach Bot ===")
print("Type 'exit' to quit.\n")

# Agent chaining: start with mood inquiry
print("Coach: How do you feel today?")
initial_input = input("You: ").strip()

try:
    # Chain 1: Analyze mood
    mood = analyze_mood.func(initial_input)
    print("Coach:", mood)

    # Chain 2: Route based on mood
    if "NEGATIVE" in mood:
        suggestion = suggest_meditation.func(initial_input)
    elif "POSITIVE" in mood:
        suggestion = journaling_prompt.func(initial_input)
    else:
        suggestion = send_affirmation.func(initial_input)

    print("Coach Suggestion:", suggestion)

except Exception as e:
    print("Coach: Something went wrong:", str(e))

# Continue chat loop
while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() == "exit":
        print("\nCoach: Take care of yourself 🧘‍♂️")
        break

    try:
        response = agent.run(user_input)
        print("Coach:", response)
    except Exception as e:
        print("Coach: Something went wrong:", str(e))
