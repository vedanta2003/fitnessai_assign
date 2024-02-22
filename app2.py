import streamlit as st
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """ENSURE TO INTAKE user body type, fitness goals and dietary restrictions before recommending. If user details are already mentioned previously in chat
REMEMBER the user's details and then the response should be concise and helpful mimicking a fitness assistant.
INPUT = """

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Create a folder named "logs" to store chat history
logs_folder = "logs"
os.makedirs(logs_folder, exist_ok=True)

def generate_gemini_response(input, prompt):
    response = chat.send_message(prompt + input)
    return response

user_id = st.text_input("User ID:")
if not user_id:
    st.warning("Please enter a User ID.")
    st.stop()

user_logs_folder = os.path.join(logs_folder, user_id)
os.makedirs(user_logs_folder, exist_ok=True)

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

st.header("FitnessAI")
input_text = st.text_input("Hi! How can I help your journey towards a healthy life?")
submit = st.button("Process")

if submit and input_text:
    with st.spinner("Processing"):
        response = generate_gemini_response(input_text, prompt)
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
            
        # Save chat history to user's logs folder
        with open(os.path.join(user_logs_folder, "chat_history.txt"), "a") as file:
            for role, text in st.session_state['chat_history']:
                file.write(f"{role}: {text}\n")

    st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
