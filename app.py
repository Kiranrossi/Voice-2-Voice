import streamlit as st
import uuid
import os

# --- Import Backend Services Directly (Monolith) --- 
from backend.services.speech import transcribe_audio
from backend.services.llm import generate_response
from backend.services.audio import text_to_speech

# --- Page Config ---
st.set_page_config(
    page_title="Voice2Voice.Ai",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Session State Management ---
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Key to force reset of audio widget
if 'audio_key' not in st.session_state:
    st.session_state.audio_key = 0

# --- Custom CSS for Layout ---
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #121212; /* Deep Black */
        color: #FFFFFF;
    }
    
    /* Title Style */
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        color: #4facfe;
        text-align: center;
        margin-bottom: 2rem;
        background: -webkit-linear-gradient(#4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Message Wrapper (Flexbox for vertical stacking) */
    .msg-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;
        width: 100%;
        max-width: 80%;
    }
    
    /* User Alignment: Right */
    .user-container {
        align-items: flex-end;
        margin-left: auto; /* Push to right */
    }
    
    /* AI Alignment: Left */
    .ai-container {
        align-items: flex-start;
        margin-right: auto; /* Push to left */
    }

    /* Text Bubbles */
    .chat-bubble {
        padding: 15px 20px;
        border-radius: 15px;
        font-size: 16px;
        line-height: 1.5;
        margin-bottom: 8px; /* Space between text and audio */
        color: white;
        word-wrap: break-word;
    }

    .user-bubble {
        background-color: #2563EB; /* Bright Blue */
        border-bottom-right-radius: 2px;
        text-align: right;
    }

    .ai-bubble {
        background-color: #2D3748; /* Dark Grey */
        border-bottom-left-radius: 2px;
        text-align: left;
    }

    /* Audio Player Styling Override */
    .stAudio {
        width: 300px !important; /* Fixed width for players */
    }
    
    /* Hide Default Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="main-title">Voice2Voice.Ai</div>', unsafe_allow_html=True)

# --- Reset Button ---
if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = []
    st.session_state.audio_key += 1 # Reset input
    st.rerun()

# --- Chat History Render ---
# We use a container to hold messages
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            # --- USER MESSAGE (RIGHT) ---
            # Using HTML for Alignment + Streamlit Audio
            # We use a 2-column trick to push content to the right
            
            c1, c2 = st.columns([0.2, 0.8])
            with c2:
                # Text Bubble (Right Aligned via CSS)
                st.markdown(f"""
                <div class="msg-container user-container">
                    <div class="chat-bubble user-bubble">
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Audio Player (Below Text, Right Aligned via Streamlit layout)
                if message.get("audio"):
                    # Push audio player to the right side
                    c2_left, c2_right = st.columns([0.7, 0.3])
                    with c2_right:
                         st.audio(message["audio"], format="audio/wav", start_time=0)

        else:
            # --- AI MESSAGE (LEFT) ---
            c1, c2 = st.columns([0.8, 0.2])
            with c1:
                 # Text Bubble (Left Aligned via CSS)
                st.markdown(f"""
                <div class="msg-container ai-container">
                     <div class="chat-bubble ai-bubble">
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Audio Player (Below Text)
                if message.get("audio"):
                     st.audio(message["audio"], format="audio/mp3", start_time=0)

st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True) # Spacer

# --- Audio Input Logic ---
st.markdown("---")

# Use dynamic key to reset widget
audio_key = f"audio_input_{st.session_state.audio_key}"
audio_value = st.audio_input("Tap Microphone to Record", key=audio_key)

if audio_value is not None:
    # Processing Logic
    with st.status("Processing...", expanded=True) as status:
        try:
            # 1. Transcribe
            status.write("👂 Listening...")
            temp_filename = f"temp_{uuid.uuid4()}.wav"
            with open(temp_filename, "wb") as f:
                f.write(audio_value.read())
            
            user_text = transcribe_audio(temp_filename)
            
            # Cleanup temp file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            
            if user_text:
                status.write(f"📝 Heard: {user_text}")
                
                # 2. LLM
                status.write("🧠 Thinking...")
                try:
                    ai_text = generate_response(st.session_state.session_id, user_text)
                except Exception as llm_error:
                     # Check for specific error related to decommissioning or otherwise
                     # Fallback logic or error report
                     ai_text = "I apologize, but I'm having trouble thinking right now due to a connection issue with my brain (LLM)."
                     print(f"LLM Error: {llm_error}")

                # 3. TTS
                status.write("🗣️ Speaking...")
                audio_bytes = text_to_speech(ai_text)
                
                # Check if audio_bytes is None (Quota Exceeded or Error)
                if not audio_bytes:
                    status.write("⚠️ Voice generation failed (likely quota limit).")
                
                # Update History
                audio_value.seek(0)
                user_audio_bytes = audio_value.read()
                
                st.session_state.messages.append({
                    "role": "user", 
                    "content": user_text,
                    "audio": user_audio_bytes
                })
                # Only add audio if it exists
                ai_msg = {
                    "role": "assistant", 
                    "content": ai_text
                }
                if audio_bytes:
                    ai_msg["audio"] = audio_bytes
                    
                st.session_state.messages.append(ai_msg)
                
                status.update(label="Response Ready!", state="complete", expanded=False)
                
                # INCREMENT KEY TO RESET INPUT
                st.session_state.audio_key += 1
                st.rerun()
            else:
                 status.update(label="No speech detected", state="error")

        except Exception as e:
            status.update(label="Error processing", state="error")
            st.error(f"Error: {e}")
