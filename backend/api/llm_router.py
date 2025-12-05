"""
LLM API Router
Endpoints for Language Model tasks (Summarization, Text Generation)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from models.summarization_model import summarization_model

router = APIRouter()

class SummarizationRequest(BaseModel):
    text: str
    max_length: Optional[int] = 150
    min_length: Optional[int] = 30

class SummarizationResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    model: str

class TextGenerationRequest(BaseModel):
    prompt: str
    max_length: Optional[int] = 200
    temperature: Optional[float] = 0.7

class TextGenerationResponse(BaseModel):
    generated_text: str
    prompt: str
    model: str

@router.post("/summarize", response_model=SummarizationResponse)
async def summarize_text(request: SummarizationRequest):
    """
    Summarize Khmer text
    
    Args:
        request: SummarizationRequest with text and parameters
        
    Returns:
        SummarizationResponse with summary
    """
    try:
        result = summarization_model.summarize_text(
            request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
        return SummarizationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

@router.post("/generate", response_model=TextGenerationResponse)
async def generate_text(request: TextGenerationRequest):
    """
    Generate text from prompt
    
    Args:
        request: TextGenerationRequest with prompt and parameters
        
    Returns:
        TextGenerationResponse with generated text
    """
    try:
        result = summarization_model.generate_text(
            request.prompt,
            max_length=request.max_length
        )
        
        return TextGenerationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text generation failed: {str(e)}")

@router.get("/models")
async def get_available_models():
    """Get list of available LLM models"""
    return {
        "models": [
            {
                "name": "Seanghay/khmer-mt5-summarization",
                "type": "mT5",
                "task": "Summarization",
                "description": "Fine-tuned mT5 for Khmer text summarization"
            },
            {
                "name": "PrahokBART",
                "type": "BART",
                "task": "Seq2Seq",
                "description": "BART model for summarization, headline generation, translation",
                "year": 2025,
                "paper": "ACL Anthology"
            },
            {
                "name": "SEA LION Khmer LLM",
                "type": "7B LLM",
                "task": "General text generation",
                "description": "Cambodia-Singapore project",
                "status": "upcoming"
            }
        ],
        "current_model": "Seanghay/khmer-mt5-summarization"
    }

@router.get("/health")
async def health_check():
    """Check if LLM service is available"""
    return {"status": "healthy", "service": "LLM"}
