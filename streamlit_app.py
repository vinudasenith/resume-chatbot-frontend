import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="Chatbot Frontend", layout="centered")


# Title
st.title("🤖 AI Assistant")


# add conversation state
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat input
if prompt := st.chat_input("Ask something..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    # Send user message to backend
    try:
        response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={"message": prompt},
    headers={"Content-Type": "application/json"}
)

        response.raise_for_status()
        result = response.json()
        bot_response = result.get("response", "No response from server.")
    except Exception as e:
        bot_response = f"⚠️ Error: {e}"


    # Display ai response
    with st.chat_message("assistant"):
        st.markdown(bot_response)


    # Store ai response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
