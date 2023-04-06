import streamlit as st # import the Streamlit library for building web applications

import openai # import the OpenAI library for interfacing with the OpenAI API

from pathlib import Path # import the pathlib library for working with file paths

import pyttsx3 # import the pyttsx3 library for converting text to speech

import speech_recognition as sr # import the speech_recognition library for performing speech recognition




openai.api_key = "Insert api key here"

engine = "text-davinci-003"
temperature = 0.6
max_tokens = 150

def askGPT(text): # Define a function called "askGPT" that takes a text input
    response = openai.Completion.create( # Use the OpenAI Completion API to generate a response to the input text
        engine = engine, # Specify the OpenAI engine to use (presumably defined elsewhere in the code)
        prompt = text, # Pass the input text as the prompt for the OpenAI model
        temperature = temperature, # Specify the temperature parameter for the OpenAI model (presumably defined elsewhere in the code)
        max_tokens = max_tokens # Specify the maximum number of tokens in the generated response (presumably defined elsewhere in the code)
    )
    return response.choices[0].text
    

def text_to_speech(text): # Define a function called "text_to_speech" that takes a text input
    engine = pyttsx3.init() # Initialize a pyttsx3 engine object for text-to-speech conversion
    engine.setProperty('rate', 150) # Set the speaking rate of the engine to 150 words per minute (can be changed as needed)
    engine.say(text) # Use the engine to convert the input text to speech
    engine.runAndWait() # Wait for the engine to finish speaking before continuing with the rest of the program

def text_to_text():
    # Define a function called "text_to_text" that takes no input parameters
    
    myQn = st.text_input("You: ", key='text_input', max_chars=None, placeholder="type here")
    # Use the Streamlit text_input widget to create a text input field with a label "You:"
    # The "key" parameter is used to keep the widget state persistent across reruns of the Streamlit app
    # The "max_chars" parameter is set to None to allow any number of characters to be entered
    # The "placeholder" parameter is used to show a placeholder text inside the input field
    
    return myQn
    # Return the value of the "myQn" variable (which contains the text input from the user)


def speech_to_text():
    # Define a function called "speech_to_text" that takes no input parameters
    
    r = sr.Recognizer()
    # Create a new speech_recognition Recognizer object called "r"
    
    with sr.Microphone() as source:
        # Use the speech_recognition Microphone class to capture audio from the default system microphone
        print("Speak:") # Print the message "Speak:" to the console to prompt the user to speak
        audio = r.listen(source, timeout=2, phrase_time_limit=5)
        # Use the Recognizer object to listen to the audio from the microphone for a maximum of 2 seconds
        # The "phrase_time_limit" parameter is set to 5 seconds to limit the maximum length of a single phrase
        
    myQn = "" # Initialize an empty string variable called "myQn"
    
    try:
        myQn = r.recognize_google(audio) # Use the Google Speech Recognition API to transcribe the audio to text
        st.write("You:", myQn) # Use the Streamlit write function to print the recognized text to the app
    except sr.UnknownValueError:
        st.write('Error') # If the Recognizer is unable to recognize the audio, print the message "Error" to the app
        
    return myQn
    # Return the value of the "myQn" variable (which contains the recognized text from the user's speech)



voice = st.button("Speak", key="Start")
texts = st.button("Write", key="Write")

# Use the Streamlit button widgets to create two buttons with labels "Speak" and "Write"
# The "key" parameter is used to keep the widget state persistent across reruns of the Streamlit app

if voice: # If the "Speak" button is clicked
    text = speech_to_text() # Call the "speech_to_text" function to transcribe the user's speech to text
else: # If the "Speak" button is not clicked
    text = text_to_text() # Call the "text_to_text" function to get text input from the user

if text == "": # If the user did not input any text
    response = "Can't understand you." # Set the response variable to the error message "Can't understand you."
else: # If the user inputted text
    response = askGPT(text) # Call the "askGPT" function to generate a response based on the user's input


st.write('Bot:', response)
# Use the Streamlit text area widget to display the text "Oliver:" and the value of the "response" variable

st.button("Submit", key="sub")
# Use the Streamlit button widget to create a "Submit" button with a "key" parameter set to "sub"

speech_button = st.button("Listen to Answer")
# Use the Streamlit button widget to create a "Listen to Answer" button, and store its state in the "speech_button" variable

if speech_button: # If the "Listen to Answer" button is clicked
    text_to_speech(response) # Call the "text_to_speech" function to speak the contents of the "response" variable


