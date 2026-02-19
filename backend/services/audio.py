import requests
from backend.config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
from gtts import gTTS
import io

def text_to_speech(text: str) -> bytes:
    """
    Converts text to audio using:
    1. ElevenLabs (Professional)
    2. Fallback to gTTS (Free) if ElevenLabs fails (quota exceeded)
    """
    # Try ElevenLabs First
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.content
        
        elif response.status_code == 429 or "quota_exceeded" in response.text:
             print("ElevenLabs Quota Exceeded. Switching to gTTS (Free).")
             # Fallthrough to gTTS
             
        else:
            print(f"Error from ElevenLabs: {response.text}")
            # Fallthrough to gTTS
            
    except Exception as e:
        print(f"Error in ElevenLabs TTS: {e}")
        # Fallthrough to gTTS

    # --- FALLBACK: gTTS (Google Text-to-Speech) ---
    try:
        print("Using gTTS fallback...")
        tts = gTTS(text=text, lang='en', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception as e:
        print(f"Error in gTTS fallback: {e}")
        return None
