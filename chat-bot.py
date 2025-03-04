import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configuration for response generation
generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 256,
    "response_mime_type": "text/plain",
}

# Initialize model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

# Streamlit UI
st.title('😎Chat-Bot')

# Initialize session history if not exists
if "history" not in st.session_state:
    st.session_state.history = []

# Get user input
user_input = st.chat_input("Enter a prompt")

if user_input:
    # Start a chat session with history
    chat_session = model.start_chat(
    history=st.session_state.history
    )

    # Get response from AI
    response = chat_session.send_message(user_input)

    # Store messages in session state
    st.session_state.history.append({"role": "user", "parts": [user_input]})
    st.session_state.history.append({"role": "assistant", "parts": [response.text]})

# Display chat history
for message in st.session_state.history:
    role = message["role"]
    content = message["parts"][0]
    st.chat_message(role).write(content)
