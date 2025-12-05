"""
OCR API Router
Endpoints for Optical Character Recognition
"""
from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional
from models.ocr_model import ocr_model
import tempfile

router = APIRouter()

class OCRResponse(BaseModel):
    text: str
    language: str
    model: str
    confidence: Optional[float] = None

@router.post("/extract", response_model=OCRResponse)
async def extract_text(file: UploadFile = File(...)):
    """
    Extract Khmer text from uploaded image
    
    Args:
        file: Image file to process (JPEG, PNG, etc.)
        
    Returns:
        OCRResponse with extracted text
    """
    try:
        # Read file contents
        contents = await file.read()
        
        # Process with OCR model
        result = ocr_model.extract_text(image_bytes=contents)
        
        return OCRResponse(
            text=result["text"],
            language=result["language"],
            model=result["model"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

@router.get("/models")
async def get_available_models():
    """Get list of available OCR models"""
    return {
        "models": [
            {
                "name": "songhieng/khmer-trocr-ocr-v1.0",
                "type": "TrOCR",
                "description": "Vision Transformer + RoBERTa fine-tuned for Khmer",
                "use_case": "ID cards, documents, printed text"
            },
            {
                "name": "Khmer-OCR-Tool",
                "type": "CRAFT + TrOCR",
                "description": "2.82% CER on synthetic data",
                "github": "https://github.com/example/khmer-ocr-tool"
            }
        ],
        "current_model": "songhieng/khmer-trocr-ocr-v1.0"
    }

@router.get("/health")
async def health_check():
    """Check if OCR service is available"""
    return {"status": "healthy", "service": "OCR"}
