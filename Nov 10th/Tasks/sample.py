import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# ------------------------------
# 1️⃣ Load environment variables
# ------------------------------
load_dotenv()  # loads .env values
print("OpenRouter Key:", os.getenv("OPENROUTER_API_KEY"))


# Fetch OpenRouter API key
openrouter_key = os.getenv("OPENROUTER_API_KEY")

# --------------------------------------
# 2️⃣ Set LangChain tracing environment
# --------------------------------------
os.environ["LANGCHAIN_API_KEY"] = "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"   # replace with your actual key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "MyMistralTest"

# ------------------------------
# 3️⃣ Streamlit UI setup
# ------------------------------
st.set_page_config(page_title="Mistral Chat via OpenRouter", layout="centered")
st.title("🤖 Mistral Chat (OpenRouter + LangChain)")

st.markdown(
    """
    <style>
    body {background-color: #f5f5f5;}
    .stTextArea textarea {font-size: 16px;}
    </style>
    """,
    unsafe_allow_html=True
)

user_input = st.text_area("Enter your message:", placeholder="Ask me anything...")

# ------------------------------
# 4️⃣ Initialize LLM (Mistral)
# ------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_key
)

# ------------------------------
# 5️⃣ Define LangChain pipeline
# ------------------------------
prompt = ChatPromptTemplate.from_template("{query}")
parser = StrOutputParser()
chain = prompt | llm | parser

# ------------------------------
# 6️⃣ Handle user input
# ------------------------------
if st.button("Generate Response"):
    if user_input.strip():
        with st.spinner("💭 Mistral is thinking..."):
            try:
                result = chain.invoke({"query": user_input})
                st.success("Response:")
                st.write(result)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
    else:
        st.warning("Please enter a message first.")
