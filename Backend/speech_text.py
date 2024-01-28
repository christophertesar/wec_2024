import assemblyai as aai
from gtts import gTTS
import os

# Replace with your API key
aai.settings.api_key = "API_KEY"


def transcribe_audio_to_text(audio_file_url, output_text_file):
    # Initialize the transcriber
    transcriber = aai.Transcriber()

    # Transcribe the audio file
    transcript = transcriber.transcribe(audio_file_url)

    # Get the transcribed text
    transcribed_text = transcript.text

    # Save the transcribed text to the text file
    with open(output_text_file, 'w', encoding='utf-8') as file:
        file.write(transcribed_text)

    print("Transcription saved as:", output_text_file)
    return transcribed_text


def convert_text_to_speech(input_file, output_audio_file):
    # Convert the transcribed text to speech using gTTS
    text = ""
    with open(input_file, 'r') as file:
        text= file.read().replace('\n', '')
    tts = gTTS(text, lang='en')

    # Save the speech as an audio file
    tts.save(output_audio_file)

    print("Text-to-speech saved as:", output_audio_file)

# URL of the file to transcribe
# audio_file_url = 'C:/Users/manra/OneDrive/Documents/Sound Recordings/Recording.m4a'

# Define the path and name for the output text file
# text_output_path = 'C:/Users/manra/OneDrive/Desktop/voice_notes/Recording_transcription.txt'

# Define the path and name for the output audio file
# audio_output_path = 'C:/Users/manra/OneDrive/Desktop/voice_notes/Recording_transcription.mp3'

# Transcribe the audio to text
# transcribed_text = transcribe_audio_to_text(audio_file_url, text_output_path)

# Convert the text to speech
# convert_text_to_speech(transcribed_text, audio_output_path)

# Optionally, play the generated speech
# os.system(f'start {audio_output_path}')
