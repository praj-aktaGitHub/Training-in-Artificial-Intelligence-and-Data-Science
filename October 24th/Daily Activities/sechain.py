import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------------------------------------------------
# 1. Load environment variables
# ----------------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# ----------------------------------------------------------
# 2. Initialize model (Mistral via OpenRouter)
# ----------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)

# ----------------------------------------------------------
# 3. Define prompt templates
# ----------------------------------------------------------
summary_prompt = ChatPromptTemplate.from_template(
    "<s>[INST] You are a concise assistant. Explain {topic} in simple terms for a beginner. [/INST]"
)

quiz_prompt = ChatPromptTemplate.from_template(
    "<s>[INST] Based on the following summary, generate 3 beginner-level quiz questions:\n\n{summary} [/INST]"
)

parser = StrOutputParser()

# ----------------------------------------------------------
# 4. Chain functions
# ----------------------------------------------------------
def generate_summary(topic):
    chain = summary_prompt | llm | parser
    return chain.invoke({"topic": topic})

def generate_quiz(summary):
    chain = quiz_prompt | llm | parser
    return chain.invoke({"summary": summary})

# ----------------------------------------------------------
# 5. Execution
# ----------------------------------------------------------
user_topic = input("Enter a topic: ").strip()
summary = generate_summary(user_topic)
quiz = generate_quiz(summary)

print("\n Summary:\n", summary)
print("\n Quiz Questions:\n", quiz)

# ----------------------------------------------------------
# 6. Logging
# ----------------------------------------------------------
os.makedirs("logs", exist_ok=True)
log_entry = {
    "timestamp": datetime.now().isoformat(),
    "topic": user_topic,
    "summary": summary,
    "quiz": quiz
}
with open("logs/sequential_log_chain.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(log_entry) + "\n")

print("\n Results logged to logs/sequential_log_chain.jsonl")
