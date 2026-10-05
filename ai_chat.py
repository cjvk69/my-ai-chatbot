import streamlit as st
from groq import Groq

# --- Page setup ---
st.set_page_config(page_title="My Free AI Chatbot", page_icon="🤖")
st.title("🤖 My Free AI Chatbot")
st.caption("Powered by free Groq models • Completely free to use")

# --- API Key ---
api_key = st.sidebar.text_input("Groq API Key", type="password", help="Get one free at console.groq.com")

if not api_key:
    st.info("👈 Enter your free Groq API key in the sidebar to start chatting")
    st.stop()

client = Groq(api_key=api_key)

# --- Model selection ---
model = st.sidebar.selectbox(
    "Choose a free model",
    [
        "openai/gpt-oss-20b",          # Fastest & recommended
        "openai/gpt-oss-120b",         # Stronger quality
        "qwen/qwen3.8-27b"             # Another good free option
    ]
)

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your free AI assistant. What would you like to talk about?"}
    ]

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input ---
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=0.7,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    # Save AI reply
    st.session_state.messages.append({"role": "assistant", "content": reply})