# Voice-to-Voice AI Project Plan

## 🏗 Phase 1: Environment & Setup
- [x] **Project Structure Creation**: Create `backend/`, `frontend/`, `models/`, `utils/` folders.
- [x] **Environment Variables**: Create `.env` file for `GROQ_API_KEY` and `ELEVENLABS_API_KEY`.
- [x] **Dependencies**: Create `requirements.txt` with `fastapi`, `uvicorn`, `streamlit`, `groq`, `requests`, `python-dotenv`.
- [x] **Virtual Environment**: Set up and activate a Python virtual environment.

## 🧠 Phase 2: Backend Development (FastAPI)
- [x] **FastAPI Setup**: Initialize `backend/main.py` with basic health check.
- [x] **Groq Client (STT)**: Implement `services/speech_to_text.py` using Groq Whisper.
- [x] **Memory Manager**: Implement `services/memory_manager.py` using strictly typed Python objects (mimicking Redis).
- [x] **Groq Client (LLM)**: Implement `services/llm_chat.py` with system prompt and history injection.
- [x] **ElevenLabs Client (TTS)**: Implement `services/text_to_speech.py` using your Voice ID.
- [x] **API Endpoint**: Create `POST /chat` endpoint to orchestrate Audio → Text → LLM → Audio.
- [x] **CORS Middleware**: Configure CORS to allow Streamlit requests.

## 🎨 Phase 3: Frontend Development (Streamlit)
- [x] **UI Layout**: Create `frontend/app.py` with a clean, professional interface.
- [x] **Audio Recorder**: Implement microphone recording functionality.
- [x] **API Integration**: Connect Streamlit to FastAPI backend (`requests.post`).
- [x] **Audio Playback**: Auto-play the returned MP3 audio.
- [x] **Chat Interface**: Display the text conversation history (User vs Assistant).

## 🚀 Phase 4: Production Polish & Optimization
- [ ] **Error Handling**: Add try-catch blocks for API failures (Groq/ElevenLabs).
- [ ] **Latency Check**: optimizing buffer sizes for faster response.
- [ ] **Logging**: Add structural logging to track requests.
- [ ] **Documentation**: Write `README.md` with usage instructions.
