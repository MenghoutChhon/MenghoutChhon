"""
LLM API Router
Using PrahokBART and mT5 for Khmer text summarization and generation
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from models.llm_model import KhmerLLM

router = APIRouter()
llm_model = None

class SummarizationRequest(BaseModel):
    text: str
    max_length: Optional[int] = 150
    min_length: Optional[int] = 50

class GenerationRequest(BaseModel):
    prompt: str
    max_length: Optional[int] = 200
    temperature: Optional[float] = 0.7

class LLMResponse(BaseModel):
    output: str
    input_length: int
    output_length: int

@router.on_event("startup")
async def load_model():
    """Load LLM models on startup"""
    global llm_model
    try:
        llm_model = KhmerLLM()
        print("LLM models loaded successfully")
    except Exception as e:
        print(f"Error loading LLM models: {e}")

@router.post("/summarize", response_model=LLMResponse)
async def summarize_text(request: SummarizationRequest):
    """
    Summarize Khmer text
    
    Args:
        request: SummarizationRequest with text and length parameters
    
    Returns:
        Summarized text
    """
    if not llm_model:
        raise HTTPException(status_code=503, detail="LLM model not loaded")
    
    try:
        summary = llm_model.summarize(
            text=request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
        return LLMResponse(
            output=summary,
            input_length=len(request.text),
            output_length=len(summary)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

@router.post("/generate", response_model=LLMResponse)
async def generate_text(request: GenerationRequest):
    """
    Generate Khmer text based on prompt
    
    Args:
        request: GenerationRequest with prompt and generation parameters
    
    Returns:
        Generated text
    """
    if not llm_model:
        raise HTTPException(status_code=503, detail="LLM model not loaded")
    
    try:
        generated = llm_model.generate(
            prompt=request.prompt,
            max_length=request.max_length,
            temperature=request.temperature
        )
        
        return LLMResponse(
            output=generated,
            input_length=len(request.prompt),
            output_length=len(generated)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text generation failed: {str(e)}")

@router.get("/status")
async def get_status():
    """Get LLM model status"""
    return {
        "model_loaded": llm_model is not None,
        "models": {
            "summarization": "khmer-mt5-summarization",
            "generation": "PrahokBART"
        } if llm_model else None,
        "supported_language": "Khmer"
    }
