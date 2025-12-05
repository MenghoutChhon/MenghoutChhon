"""
TTS API Router
Endpoints for Text-to-Speech conversion
"""
from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import tempfile
import os
from models.tts_model import tts_model

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    language: str = "khmer"

class TTSResponse(BaseModel):
    message: str
    sample_rate: int
    duration: float
    text: str
    audio_file: Optional[str] = None

@router.post("/synthesize", response_model=TTSResponse)
async def synthesize_speech(request: TTSRequest):
    """
    Convert Khmer text to speech
    
    Args:
        request: TTSRequest with text to convert
        
    Returns:
        TTSResponse with audio metadata and file path
    """
    try:
        # Create temporary file for audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            output_path = tmp_file.name
        
        # Generate speech
        result = tts_model.generate_speech(request.text, output_path)
        
        return TTSResponse(
            message="Speech generated successfully",
            sample_rate=result["sample_rate"],
            duration=result["duration"],
            text=result["text"],
            audio_file=output_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

@router.get("/download/{filename}")
async def download_audio(filename: str):
    """
    Download generated audio file
    
    Args:
        filename: Name of the audio file to download
        
    Returns:
        FileResponse with audio file
    """
    file_path = f"/tmp/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(file_path, media_type="audio/wav", filename=filename)

@router.get("/models")
async def get_available_models():
    """Get list of available TTS models"""
    return {
        "models": [
            {
                "name": "facebook/mms-tts-khm",
                "language": "Khmer",
                "type": "VITS",
                "description": "Meta's Massively Multilingual Speech model for Khmer"
            },
            {
                "name": "mrrtmob/khmer-tts",
                "language": "Khmer",
                "type": "Tacotron 2",
                "description": "Tacotron 2 model for Khmer TTS"
            }
        ],
        "current_model": "facebook/mms-tts-khm"
    }
