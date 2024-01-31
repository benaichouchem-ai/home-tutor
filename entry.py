from pathlib import Path
from openai import OpenAI
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import argparse
import configparser

# Set up OpenAI API
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config.get('DEFAULT', 'API_KEY')
client = OpenAI(
    api_key=api_key        
)


# Function to convert text to speech
def homeWorker_tutor(text):
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello world"}]
)

def text_to_speech(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text

    )
    with open(speech_file_path, "wb") as f:
        f.write(response.content)

# Function to record audio
def record_audio(duration):
    fs = 44100  # Sample rate
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording)  # Save as WAV file 

# Function to convert speech to text
def speech_to_text():
    record_audio(5)  # Record 5 seconds of audio
    audio_file= open("output.wav", "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )

    return transcript

parser = argparse.ArgumentParser(description="Homework Helper")
parser.add_argument("command", choices=["text_to_speech", "record_audio", "speech_to_text"], help="The command to execute")
args = parser.parse_args()

if args.command == "text_to_speech":
    text = input("Enter the text to convert to speech: ")
    text_to_speech(text)
    print("Speech generated successfully.")
elif args.command == "record_audio":
    duration = float(input("Enter the duration in seconds: "))
    record_audio(duration)
    print("Audio recorded successfully.")
elif args.command == "speech_to_text":
    result = speech_to_text()
    print(result)
