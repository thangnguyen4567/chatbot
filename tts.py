import openai
import pyttsx3
import os
import uuid
import json
from datetime import datetime
from dotenv import load_dotenv
# from gtts import gTTS #text-to-speech
# import pygame #play audio file

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# File to store recordings
recordings_file = 'recordings.json'

# Load existing recordings
if os.path.exists(recordings_file):
    with open(recordings_file, 'r') as file:
        recordings = json.load(file)
else:
    recordings = []



script_dir = os.path.dirname(os.path.realpath(__file__))
directory = "AudioFolder"
# Create the full path
path = os.path.join(script_dir, directory)
if not os.path.exists(path):
    os.mkdir(path)

# # Adjectives and nouns to generate random names for voices
# adjectives = ["beautiful", "sad", "mystical", "serene", "whispering", "gentle", "melancholic"]
# nouns = ["sea", "love", "dreams", "song", "rain", "sunrise", "silence", "echo"]

# Initializing pyttsx3 for text-to-speech output

def change_voice(engine, language, gender='VoiceGenderFemale'):
    voices = engine.getProperty('voices')
    for voice in voices:
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True
    # print(f"Desired voice with language '{language}' and gender '{gender}' not found. Using default voice.")
    return False

def speech_to_text(audio_path):
    print("entered transcribe", "./" + audio_path)
    audio_file = open(audio_path, "rb")
    print(audio_file)
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # print(transcript) //debug
    return transcript['text']

 #tạo file mp3
def text_to_speech(response, directory = "AudioFolder/"):
    engine = pyttsx3.init()
    audioId = str(uuid.uuid4())
    audioFileName = "//" + audioId + ".mp3"
    directory += audioFileName
    directory = os.path.normpath(directory)
    engine.save_to_file(response, directory)
    engine.runAndWait()
    return audioId

# def text_to_speech(response):
#     text_to_speech = gTTS(text=response) #đọc ra
#     text_to_speech.save("chatbot_audio.mp3") #save audio to mp3 file
#     pygame.mixer.music.load("chatbot_audio.mp3") #load mp3 file
#     pygame.mixer.music.play() #play audio

# def save_response_to_file(response, folder="responses"):
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#     response_filename = os.path.join(folder, f"response_{len(os.listdir(folder)) + 1}.txt")
#     with open(response_filename, 'w') as f:
#         f.write(response)
#     print(f"Response saved to {response_filename}")

def openai_chat_send(transcript):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": transcript}
    ]
    print("Transcript:", transcript)
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return completion.choices[0].message.content

def record_response(question, response):
    timestamp = datetime.now().isoformat()
    recording = {
        'timestamp': timestamp,
        'question': question,
        'response': response
    }
    recordings.append(recording)
    with open(recordings_file, 'w') as file:
        json.dump(recordings, file, indent=4)
    print(f"Recording saved: {recording}")




# question = input("Type your question: ")

# # Send user input to OpenAI ChatGPT
# response = openai_chat_send(question)

# # Print the assistant's response
# print("Assistant:", response)

# # Convert output to voice
# text_to_speech(response)

# # Record the response
# record_response(question, response)
