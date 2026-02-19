import streamlit as st
import requests
import uuid
import base64

# --- Page Config ---
st.set_page_config(
    page_title="Voice Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Constants ---
API_URL = "http://localhost:8000/api/process-audio"

# --- Session State ---
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'last_audio' not in st.session_state:
    st.session_state.last_audio = None

# --- Custom CSS for "ChatGPT-like" UI ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #212121;
        color: #ECECEC;
    }
    
    /* Remove standard Streamlit top padding/headers */
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 10rem; /* Space for fixed footer */
    }

    /* Fixed Bottom Input Area */
    .fixed-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #212121; /* Match background */
        border-top: 1px solid #333;
        padding: 20px 50px;
        z-index: 1000;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Chat Bubbles */
    .stChatMessage {
        background-color: transparent !important;
    }
    
    /* User Avatar */
    .stChatMessage.user .avatar {
        background-color: #ECECEC;
    }
    
    /* Assistant Avatar */
    .stChatMessage.assistant .avatar {
        background-color: #10a37f;
    }
    
    /* Audio Player Styling */
    .stAudio {
        margin-top: 10px;
        width: 100%;
    }
    
    /* Hide 'Deploy' button */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h3 style='text-align: center; color: #ECECEC; margin-bottom: 30px;'>🎙️ Voice AI Assistant</h3>", unsafe_allow_html=True)

# --- Display Conversation ---
# We use standard container for history so it scrolls naturally
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If there is associated audio for an assistant message, play it
        if message.get("audio"):
            st.audio(message["audio"], format="audio/mp3", start_time=0)

# --- Footer Input Area ---
# We use a container to mimic the 'fixed' bottom bar
with st.container():
    st.markdown('<div class="fixed-footer">', unsafe_allow_html=True)
    
    # Grid layout for the bottom bar controls
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        # The Audio Input Widget
        audio_value = st.audio_input("Record Voice", key="audio_recorder")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- Logic: Handle Audio Input ---
if audio_value:
    # Only process if it's a new recording (prevent re-running logic on same audio)
    # Streamlit re-runs script on interaction, so audio_value will be present
    
    # Helper to prevent processing same audio twice (st.audio_input retains value)
    # real-world usage usually needs a way to 'clear' it, but st.audio_input is currently sticky.
    # We will assume if the bytes differ or we force a rerun it works. 
    # For now, simplistic handling:
    
    with st.spinner("Thinking..."):
        # 1. Display User Message Immediately (Optimistic UI)
        # Note: We can't easily get text *before* sending to backend in this architecture 
        # unless we do STT frontend side. We will wait for backend response.
        
        try:
            # Create files payload
            files = {"file": ("audio.wav", audio_value, "audio/wav")}
            data = {"session_id": st.session_state.session_id}
            
            # Call Backend
            response = requests.post(API_URL, files=files, data=data)
            
            if response.status_code == 200:
                # Extract headers
                user_text = response.headers.get("X-Transcribed-Text", "...")
                ai_text = response.headers.get("X-Response-Text", "...")
                audio_content = response.content
                
                # Append to messages state
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_text, 
                    "audio": audio_content
                })
                
                # Force Rerun to update the chat history view
                st.rerun()
                
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"Connection Error: {e}")

