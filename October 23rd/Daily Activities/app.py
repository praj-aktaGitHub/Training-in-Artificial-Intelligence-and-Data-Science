import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Streamlit config
st.set_page_config(page_title="prajBot 💖", page_icon="🤖", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #2f2f2f;
        }
        h1 {
            text-align: center;
            font-size: 3em;
        }
        .title-pink {
            color: #ffb6c1;
        }
        .user-bubble {
            background-color: #d3d3d3;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            color: black;
        }
        .bot-bubble {
            background-color: #ffe4e1;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            color: #d63384;
        }
        .footer {
            text-align: center;
            font-size: 12px;
            color: #ff69b4;
        }
        .stSidebar {
            background-color: #ffb6c1 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar settings
st.sidebar.title("⚙️ Settings")
model_choice = st.sidebar.selectbox("Choose Model", ["mistralai/mistral-7b-instruct", "openai/gpt-3.5-turbo", "meta-llama/llama-2-13b-chat"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 64, 1024, 256)

# Initialize model
llm = ChatOpenAI(
    model=model_choice,
    temperature=temperature,
    max_tokens=max_tokens,
    api_key=api_key,
    base_url=base_url,
)

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Main UI
st.markdown("<h1><span class='title-pink'>prajBot</span> Clocked IN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your personal AI assistant powered by LangChain & OpenRouter</p>", unsafe_allow_html=True)
st.markdown("---")

# Chat input
user_input = st.text_input("💬 What's cooking in that lil brain today?", placeholder="Ask me anything...")

if user_input:
    # Add user message to history
    st.session_state.chat_history.append(("user", user_input))

    # Prepare messages for model
    messages = [SystemMessage(content="You are a helpful and concise AI assistant.")]
    for role, msg in st.session_state.chat_history:
        if role == "user":
            messages.append(HumanMessage(content=f"<s>[INST] {msg} [/INST]"))

    # Get response
    with st.spinner("Thinking hard... "):
        try:
            response = llm.invoke(messages)
            st.session_state.chat_history.append(("bot", response.content.strip()))
        except Exception as e:
            st.session_state.chat_history.append(("bot", f" Error: {e}"))

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"<div class='user-bubble'><strong>You:</strong> {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'><strong>prajBot:</strong> {msg}</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p class='footer'>Made with 💖 by Praj using LangChain + OpenRouter + Streamlit</p>", unsafe_allow_html=True)
