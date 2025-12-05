"""
OCR API Router
Using TrOCR for Khmer text recognition
"""
from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import List, Optional
import base64
from models.ocr_model import KhmerOCR

router = APIRouter()
ocr_model = None

class OCRResponse(BaseModel):
    text: str
    confidence: float
    detected_lines: List[str]

async def load_model():
    """Load OCR model on startup"""
    global ocr_model
    try:
        ocr_model = KhmerOCR()
        print("OCR model loaded successfully")
    except Exception as e:
        print(f"Error loading OCR model: {e}")

@router.post("/recognize", response_model=OCRResponse)
async def recognize_text(file: UploadFile = File(...)):
    """
    Perform OCR on uploaded image containing Khmer text
    
    Args:
        file: Image file (PNG, JPG, JPEG)
    
    Returns:
        Recognized Khmer text with confidence score
    """
    if not ocr_model:
        raise HTTPException(status_code=503, detail="OCR model not loaded")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image data
        image_data = await file.read()
        
        # Perform OCR
        result = ocr_model.recognize(image_data)
        
        return OCRResponse(
            text=result['text'],
            confidence=result['confidence'],
            detected_lines=result['lines']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR recognition failed: {str(e)}")

@router.post("/recognize_base64", response_model=OCRResponse)
async def recognize_text_base64(image_base64: str):
    """
    Perform OCR on base64 encoded image
    
    Args:
        image_base64: Base64 encoded image string
    
    Returns:
        Recognized Khmer text with confidence score
    """
    if not ocr_model:
        raise HTTPException(status_code=503, detail="OCR model not loaded")
    
    try:
        # Decode base64 image
        image_data = base64.b64decode(image_base64)
        
        # Perform OCR
        result = ocr_model.recognize(image_data)
        
        return OCRResponse(
            text=result['text'],
            confidence=result['confidence'],
            detected_lines=result['lines']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR recognition failed: {str(e)}")

@router.get("/status")
async def get_status():
    """Get OCR model status"""
    return {
        "model_loaded": ocr_model is not None,
        "model_name": "songhieng/khmer-trocr-ocr-v1.0" if ocr_model else None,
        "supported_language": "Khmer"
    }
