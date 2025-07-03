import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

with open("summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "Satyanarayana Mareedu"
bot_display_name = "Satyanarayana Mareedu"

system_prompt = f"""
You are acting as {name}, answering questions on {name}'s website.
Your role is to represent {name} faithfully and professionally, 
especially regarding {name}'s career, background, skills, and experience.

When a user greets you (e.g., says "Hi" or "Hello"), please respond with a friendly introduction like "Hi, How can I help you today?" or a similar welcoming phrase.

You have access to the following context:

## Summary:
{summary}

You must answer ONLY using the information provided in the summary above. Do NOT use any outside knowledge, 
assumptions, or information not present in the context.
If you do not know the answer based on the provided context, respond with something like:
"I'm sorry, I don't have that information based on what I know. If you'd like to know more or get in touch, please use the contact details provided in the summary above."

Stay in character as {name} at all times,
and be professional and engaging, as if speaking to a potential client or future employer.
feel free to add any relevant emojies to make the conversation more engaging.
"""

welcome_message = (
    f"👋 Hi, I'm Satyanarayana Mareedu! 👨‍💻\n"
    "🎉 Welcome to my personal website!\n"
    "💬 Feel free to ask me anything about my career, skills, projects, or professional background.\n"
    "I'm here to help you learn more about me! 🚀"
)

gemini = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_bot_response(message, history):
    messages = [{"role": "system", "content": system_prompt}]
    for entry in history:
        if entry["role"] == "user":
            messages.append({"role": "user", "content": entry["content"]})
        elif entry["role"] == "assistant":
            messages.append({"role": "assistant", "content": entry["content"]})
    messages.append({"role": "user", "content": message})
    response = gemini.beta.chat.completions.parse(model="gemini-2.0-flash", messages=messages)
    return response.choices[0].message.content

st.set_page_config(page_title="Satyanarayana Mareedu", layout="centered",page_icon="👨‍💻")
st.title("Hii 👋")


st.markdown(
    """
    <style>
    header {visibility: hidden;}
    .st-emotion-cache-1cei9z1{
        paddingTop: 16px !important
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": welcome_message}
    ]

for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.spinner("Satyanarayana is typing..."):
        bot_response = get_bot_response(user_input, st.session_state.chat_history[:-1])
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response) 