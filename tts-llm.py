import sounddevice as sd
from elevenlabs import ElevenLabs
import numpy as np
import pygame
import wave
import os
import io
import tempfile
from groq import Groq


# # List available audio devices
# print(sd.query_devices())
# print("Default input device:", sd.default.device)


# Try to get API key from environment variable, fallback to hardcoded key
api_key = os.getenv("ELEVENLABS_API_KEY") or ""
groq_api_key = os.getenv("GROQ_API_KEY") or ""

client = ElevenLabs(api_key=api_key)
groq_client = Groq(api_key=groq_api_key)

#record audio
def record_audio(filename="input.wav",seconds=5,sample_rate=44100):
    print("Recording...")
    audio = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32, device=4)
    sd.wait()

    #  Save audio in wav file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes((audio*32767).astype(np.int16).tobytes())

    return filename


def transcribe(audio_file):
    try:
        with open(audio_file,"rb") as f:
            transcription=client.speech_to_text.convert(file=f,model_id="scribe_v1")
        return transcription.text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return "Error transcribing audio"


import requests

def generate_llm_response(user_input, api_url="http://127.0.0.1:8000/chatbot"):
    """
    Call the FastAPI /chatbot endpoint to get a response from the ingested documents.

    Args:
        user_input (str): The user's input text
        api_url (str): The URL of the chatbot endpoint (default is local)

    Returns:
        str: The response from the chatbot endpoint
    """
    try:
        # Send form-data POST request
        response = requests.post(
            api_url,
            data={"query": user_input}  # matches Form(...) in FastAPI endpoint
        )

        # Check for HTTP errors
        response.raise_for_status()

        # Extract results
        result_json = response.json()
        return result_json.get("results", "No response received.")

    except requests.exceptions.RequestException as e:
        print(f"Error calling chatbot endpoint: {e}")
        return f"I apologize, there was an error contacting the chatbot: {str(e)}"

def speak(text,voice_id="21m00Tcm4TlvDq8ikWAM"):
    try:
        audio=client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2"
        )
        
        temp_file=tempfile.NamedTemporaryFile(delete=False,suffix=".mp3")
        try:
            for chunk in audio:
                temp_file.write(chunk)
            temp_file.close()

            pygame.mixer.init()
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)

            pygame.mixer.music.stop()
            pygame.mixer.quit()
        finally:
            try:
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
            except PermissionError:
                pass
    except Exception as e:
        print(f"Error during text-to-speech: {e}")


# Main conversation loop
while True:
    record_audio(seconds=5)
    text_input = transcribe("input.wav")
    print(f"You said: {text_input}")

    if "exit" in text_input.lower():
        print("Exiting...")
        break
    
    # Generate LLM response
    llm_response = generate_llm_response(text_input)
    print(f"AI Response: {llm_response}")
    
    # Speak the response
    speak(llm_response)