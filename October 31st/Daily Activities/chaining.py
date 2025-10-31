import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.utilities import LLMConfig  # ✅ THIS IS THE FIX

load_dotenv()

llm = LLMConfig(
    provider="openrouter",
    model="mistralai/mistral-7b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
)





# 🧠 Agent 1: Sentiment Analyzer
sentiment_agent = Agent(
    role="Sentiment Analyzer",
    goal="Understand the user's emotional tone",
    backstory="You are a compassionate listener who detects emotional states from text.",
    llm=llm,
    verbose=True
)

# 🧘 Agent 2: Wellness Coach
wellness_agent = Agent(
    role="Wellness Coach",
    goal="Suggest a helpful activity based on the user's mood",
    backstory="You are a mental wellness coach who gives practical, calming suggestions.",
    llm=llm,
    verbose=True
)

# 💬 Agent 3: Affirmation Generator
affirmation_agent = Agent(
    role="Affirmation Generator",
    goal="Provide a motivational affirmation",
    backstory="You are a positive voice that uplifts users with short, powerful affirmations.",
    llm=llm,
    verbose=True
)

# 🧩 Tasks
sentiment_task = Task(
    description="Analyze the user's message and describe their emotional tone.",
    expected_output="A short sentence describing the user's mood.",
    agent=sentiment_agent
)

wellness_task = Task(
    description="Based on the user's mood, suggest a helpful activity like journaling, breathing, or walking.",
    expected_output="A calming suggestion tailored to the user's emotional state.",
    agent=wellness_agent
)

affirmation_task = Task(
    description="Based on the user's mood, generate a short motivational affirmation.",
    expected_output="A 1-sentence affirmation that is warm, encouraging, and under 25 words.",
    agent=affirmation_agent
)

# 🚀 Crew setup
crew = Crew(
    agents=[sentiment_agent, wellness_agent, affirmation_agent],
    tasks=[sentiment_task, wellness_task, affirmation_task],
    verbose=True
)

# 🧠 Run the chain
print("\n=== 🔗 Agent Chaining Bot ===")
user_input = input("How are you feeling today? ").strip()
result = crew.kickoff(inputs={"input": user_input})
print("\nBot:\n", result)
