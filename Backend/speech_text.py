import assemblyai as aai
from gtts import gTTS
import os

# Replace with your API key
aai.settings.api_key = "INSERTKEY"

# URL of the file to transcribe
FILE_URL = 'C:/Users/manra/OneDrive/Documents/Sound Recordings/Recording.m4a'

# Initialize the transcriber
transcriber = aai.Transcriber()

# Transcribe the audio file
transcript = transcriber.transcribe(FILE_URL)

# Get the transcribed text
transcribed_text = transcript.text

# Define the path and name for the output text file
output_path = 'C:/Users/manra/OneDrive/Desktop/voice_notes/Recording_transcription.txt'

# Save the transcribed text to the text file
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(transcribed_text)

print("Transcription saved as:", output_path)

# Convert the transcribed text to speech using gTTS
tts = gTTS(transcribed_text, lang='en')

# Define the path and name for the output audio file
audio_output_path = 'C:/Users/manra/OneDrive/Desktop/voice_notes/Recording_transcription.mp3'

# Save the speech as an audio file
tts.save(audio_output_path)

print("Text-to-speech saved as:", audio_output_path)

# Play the generated speech (optional)
os.system(f'start {audio_output_path}')
