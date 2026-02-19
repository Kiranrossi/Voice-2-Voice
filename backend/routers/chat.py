import shutil
import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
import io

from backend.services.speech import transcribe_audio
from backend.services.llm import generate_response
from backend.services.audio import text_to_speech

router = APIRouter()

@router.post("/process-audio")
async def process_audio(
    file: UploadFile = File(...),
    session_id: str = Form(...)
):
    # 1. Save uploaded file temporarily
    temp_filename = f"temp_{uuid.uuid4()}.wav"
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Transcribe Audio (STT)
        user_text = transcribe_audio(temp_filename)
        print(f"Start Processing for Session {session_id}")
        print(f"User Transcribed: {user_text}")
        
        if not user_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        # 3. Generate Response (LLM)
        ai_response_text = generate_response(session_id, user_text)
        print(f"AI Response: {ai_response_text}")
        
        # 4. Convert Response to Audio (TTS)
        audio_bytes = text_to_speech(ai_response_text)
        
        if not audio_bytes:
             raise HTTPException(status_code=500, detail="Failed to generate audio response")
             
        # Clean up temp file
        os.remove(temp_filename)
        
        # Return audio as a stream
        return StreamingResponse(
            io.BytesIO(audio_bytes), 
            media_type="audio/mpeg",
            headers={
                "X-Transcribed-Text": user_text,  # Send text back in headers for UI to display (optional hack)
                "X-Response-Text": ai_response_text
            }
        )

    except Exception as e:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=500, detail=str(e))
