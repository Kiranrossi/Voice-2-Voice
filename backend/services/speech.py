import os
from groq import Groq
from backend.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes audio file to text using Groq Whisper.
    """
    try:
        with open(file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3",
                response_format="text"
            )
        return transcription
    except Exception as e:
        print(f"Error in transcription: {e}")
        return ""
