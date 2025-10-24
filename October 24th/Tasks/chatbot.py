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
# 2. Initialize model
# ----------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)

# ----------------------------------------------------------
# 3. Setup parser
# ----------------------------------------------------------
parser = StrOutputParser()

# ----------------------------------------------------------
# 4. Chat loop with memory
# ----------------------------------------------------------
conversation_history = [
    ("system", "You are a friendly and helpful assistant. Keep the conversation flowing and remember context.")
]

print("💬 Start chatting with your personal prajBot! Type 'exit' to end.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("See ya later, keep slaying💖")
        break

    # Add user input to history
    conversation_history.append(("user", user_input))

    # Build dynamic prompt with full history
    dynamic_prompt = ChatPromptTemplate.from_messages(conversation_history)

    # Run the chain
    chain = dynamic_prompt | llm | parser
    bot_response = chain.invoke({"user_input": user_input})

    # Add bot response to history
    conversation_history.append(("ai", bot_response))

    print("prajBot:", bot_response)

    # Log the conversation turn
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "bot_response": bot_response
    }
    with open("logs/chat_memory_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
