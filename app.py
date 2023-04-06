import streamlit as st
import openai
from dotenv import load_dotenv
from pathlib import Path 
from PIL import Image
import pyttsx3
import os
import speech_recognition as sr
import SessionState

load_dotenv()

import os
openai.api_key = os.environ.get("OPENAI_API_KEY")
#openai.api_key = get_secret("openai")["api_key"]

im = Image.open('content/bot.png')
st.set_page_config(page_title="Oliver", page_icon = im)

img_path = Path.joinpath(Path.cwd(),'content')
bot = Image.open(Path.joinpath(img_path,'bot.png'))
ss = SessionState.get_session_state(is_startup=True, previous_pred=0)

engine = "text-davinci-003"
temperature = 0.6
max_tokens = 150

def askGPT(text):
    response = openai.Completion.create(
        engine = engine,
        prompt = text,
        temperature = temperature,
        max_tokens = max_tokens
    )
    if ss.is_startup:
        response = "Hi, I am Oliver and I'm happy to have you here. \nHow can I help you?"
        ss.is_startup = False
        return response
    else:
        return response.choices[0].text
    

col1, mid, col2 = st.columns([1,14,35])
with col1:
    st.title("""Oliver""")
    
with col2:
    st.image(bot, width=60) 

st.write("""
This is an NLP-trained chatbot developed to hold human-like conversations.""")

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # You can change the speaking rate here
    engine.say(text)
    engine.runAndWait()

def text_to_text():
    myQn = st.text_input("You: ", key='text_input', max_chars=None, placeholder="type here")
    return myQn

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source, timeout=2, phrase_time_limit=5)
    myQn = ""
    try:
        myQn = r.recognize_google(audio)
        st.write("You:", myQn)
    except sr.UnknownValueError:
        st.write('Error')
    return myQn


col1, col2, col3 = st.columns([1, 10, 1])

with col1:
    voice = st.button("Speak", key="Start")

with col2:
    texts = st.button("Write", key="Write")

if voice:
    text = speech_to_text()
else:
    text = text_to_text()

if text == "":
    response = "Hi, I am Oliver and I'm happy to have you here. \nHow can I help you?"
else:
    response = askGPT(text)
st.text_area('Oliver:', response)
#st.button("Submit")

col1, col2, col3 = st.columns([1, 10, 2])

with col1:
    st.button("Submit", key="sub")

with col2:
    speech_button = st.button("Listen to Answer")

#with col3:
    #speech_button = st.button("Listen to Answer")

#speech_button = st.button("Listen to Answer")
if speech_button:
    text_to_speech(response)
#st.button('refresh')


col1, col2, col3 = st.columns([1, 10, 2])
with col2:
    st.button("Refresh", key="ref")


