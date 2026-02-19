import os
from dotenv import load_dotenv

load_dotenv()

# Try to look in Streamlit secrets first (for cloud deployment)
# If not found, look in os.getenv (for local .env)
def get_secret(key):
    import streamlit as st
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass # Not running in streamlit or secrets not configured
    
    return os.getenv(key)

GROQ_API_KEY = get_secret("GROQ_API_KEY")
ELEVENLABS_API_KEY = get_secret("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = get_secret("ELEVENLABS_VOICE_ID")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env file or Streamlit secrets")

if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY is not set in .env file or Streamlit secrets")

if not ELEVENLABS_VOICE_ID:
    raise ValueError("ELEVENLABS_VOICE_ID is not set in .env file or Streamlit secrets")
