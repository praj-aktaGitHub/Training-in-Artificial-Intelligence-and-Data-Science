import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# 🔧 Function to initialize model dynamically
def get_llm(model_name="mistralai/mistral-7b-instruct", temperature=0.7, max_tokens=256):
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
        base_url=base_url,
    )

# 🧠 Function to get response from model
def get_response(prompt, model_name="mistralai/mistral-7b-instruct", temperature=0.7, max_tokens=256):
    llm = get_llm(model_name, temperature, max_tokens)
    messages = [
        SystemMessage(content="You are a helpful and concise AI assistant."),
        HumanMessage(content=f"<s>[INST] {prompt.strip()} [/INST]"),
    ]
    try:
        response = llm.invoke(messages)
        return response.content.strip() or "(no content returned)"
    except Exception as e:
        return f"❌ Error: {e}"

# 🧪 Example usage (can be removed in production)
if __name__ == "__main__":
    prompt = "Explain in simple terms how convolutional neural networks work."
    output = get_response(prompt, model_name="mistralai/mistral-7b-instruct", temperature=0.7, max_tokens=256)
    print("Assistant:", output)
