"""
Text-to-Speech API Router
Using Meta's MMS TTS for Khmer language
"""
from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional
import base64
from models.tts_model import KhmerTTS

router = APIRouter()
tts_model = None

class TTSRequest(BaseModel):
    text: str
    speed: Optional[float] = 1.0

class TTSResponse(BaseModel):
    audio_base64: str
    duration: float
    text: str

@router.on_event("startup")
async def load_model():
    """Load TTS model on startup"""
    global tts_model
    try:
        tts_model = KhmerTTS()
        print("TTS model loaded successfully")
    except Exception as e:
        print(f"Error loading TTS model: {e}")

@router.post("/synthesize", response_model=TTSResponse)
async def synthesize_speech(request: TTSRequest):
    """
    Convert Khmer text to speech
    
    Args:
        request: TTSRequest with text and optional speed parameter
    
    Returns:
        Base64 encoded audio file
    """
    if not tts_model:
        raise HTTPException(status_code=503, detail="TTS model not loaded")
    
    try:
        audio_data, duration = tts_model.synthesize(
            text=request.text,
            speed=request.speed
        )
        
        # Convert audio to base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return TTSResponse(
            audio_base64=audio_base64,
            duration=duration,
            text=request.text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {str(e)}")

@router.get("/status")
async def get_status():
    """Get TTS model status"""
    return {
        "model_loaded": tts_model is not None,
        "model_name": "facebook/mms-tts-khm" if tts_model else None,
        "supported_language": "Khmer (khm)"
    }
