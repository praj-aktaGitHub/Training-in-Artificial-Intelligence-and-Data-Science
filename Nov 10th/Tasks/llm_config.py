from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = "https://openrouter.ai/api/v1"

llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.7,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)
