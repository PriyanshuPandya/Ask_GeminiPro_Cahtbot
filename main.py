import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load Environment Variables
load_dotenv()

# Config Streamlit Page Settings
st.set_page_config(
    page_title="Ask-to-Gemini-Pro!",
    page_icon=":brain:",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set Google Gemini Pro AI Model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit
def translate_role(user_role):
    if user_role == "model":
        return "assistance"
    else:
        return user_role

# Initialize chat session in streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display title on st
st.title("🤖 Gemini-Pro Chatbot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role(message.role)):
        st.markdown(message.parts[0].text)

# Input field for User
user_prompt = st.chat_input("Ask me anything...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's Response
    with st.chat_message("assistance"):
        st.markdown(gemini_response.text)

