from flask import Flask, render_template, request
import wikipediaapi
from gtts import gTTS
import os
import pygame
import time
import pyttsx3

app = Flask(__name__)

wiki_wiki = wikipediaapi.Wikipedia('Your-App-Name/1.0 (your@email.com)', 'en', extract_format=wikipediaapi.ExtractFormat.WIKI)

# Initialize pygame mixer
pygame.mixer.init()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search_query']
        result = search_wikipedia(search_query)
        tts_text = result[:500]  # Convert the first 500 characters to speech
        audio_file_path = text_to_speech(tts_text)
        #play_audio(audio_file_path)
        return render_template('index.html', result=result, search_query=search_query)
    return render_template('index.html')

def search_wikipedia(query):
    page_py = wiki_wiki.page(query)
    if page_py.exists():
        return page_py.text
    else:
        return "No result found for {}".format(query)

def text_to_speech(text):
    try: 
        language = 'en'
        tts = gTTS(text=text, lang=language, slow=False)
        audio_file_path = "output.mp3"
        tts.save(audio_file_path)
        return audio_file_path
    except: 
        engine = pyttsx3.init("nsss")
        engine.say(text)
        engine.runAndWait()

def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Add a delay to allow the audio to play
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == '__main__':
    app.run(debug=False, port=5000)
