import streamlit as st
from groq import Groq

# --- Page setup ---
st.set_page_config(page_title="Family AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Family AI Chatbot")
st.caption("Free AI chatbot • Powered by Groq")

# --- Load API key from Streamlit Secrets ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("⚠️ API key not found. Please add it in Streamlit Cloud Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# --- Model selection ---
model = st.sidebar.selectbox(
    "Choose a free model",
    [
        "openai/gpt-oss-20b",      # Fastest - recommended
        "openai/gpt-oss-120b",     # Stronger quality
        "qwen/qwen3.8-27b"         # Another good option
    ],
    index=0
)

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your family AI assistant. How can I help you today?"}
    ]

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input ---
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
            except Exception as e:
                reply = f"Sorry, something went wrong: {str(e)}"
                st.error(reply)

    # Save AI reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
