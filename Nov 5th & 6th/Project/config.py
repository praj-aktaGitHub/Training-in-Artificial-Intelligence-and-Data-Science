from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI  # Ensure you have langchain_openai installed

# Load environment variables
load_dotenv()

# OpenRouter API configuration
api_key = os.getenv("OPENROUTER_API_KEY")  # Load the OpenRouter API key from the .env file
base_url = "https://openrouter.ai/api/v1"  # Base URL for OpenRouter

# Set up the Langchain OpenAI model (via OpenRouter)
llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",  # Choose your model from OpenRouter (for example, LLaMA model)
    temperature=0.7,
    max_tokens=512,
    api_key=api_key,  # Pass the OpenRouter API key
    base_url=base_url,  # Set base URL for OpenRouter
)

# Invoke the model to get a response
res = llm.invoke("What is the capital of India?")
print(res)  # Output the result
