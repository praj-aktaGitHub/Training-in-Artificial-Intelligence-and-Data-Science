import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Bot", page_icon="🤖")
st.title("🧠 LangGraph Bot")

query = st.text_input("Type your query...")

if st.button("Submit") and query:
    try:
        response = requests.post("http://localhost:8000/query", json={"query": query})
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Result:")
            st.write(result.get("answer", "No answer returned"))
        else:
            st.error(f"❌ Server error: {response.text}")
    except Exception as e:
        st.error(f"❌ Connection error: {e}")


