"""
Video Generation API Router
Endpoints for Text-to-Video generation
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from models.video_model import video_model

router = APIRouter()

class VideoGenerationRequest(BaseModel):
    prompt: str
    duration: Optional[int] = 5
    resolution: Optional[str] = "720p"
    fps: Optional[int] = 30

class VideoGenerationResponse(BaseModel):
    status: str
    message: str
    prompt: str
    duration: Optional[int] = None
    resolution: Optional[str] = None
    video_file: Optional[str] = None
    recommended_models: Optional[list] = None
    note: Optional[str] = None

@router.post("/generate", response_model=VideoGenerationResponse)
async def generate_video(request: VideoGenerationRequest):
    """
    Generate video from text prompt
    
    Args:
        request: VideoGenerationRequest with prompt and parameters
        
    Returns:
        VideoGenerationResponse with video metadata
    """
    try:
        result = video_model.generate_video(
            prompt=request.prompt,
            duration=request.duration,
            resolution=request.resolution
        )
        
        return VideoGenerationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

@router.get("/models")
async def get_available_models():
    """Get list of available video generation models"""
    return {
        "models": [
            {
                "name": "Wan2.2-T2V-A14B",
                "parameters": "14B (MoE)",
                "features": "5s @ 720p, cinematic quality",
                "license": "Permissive",
                "url": "https://huggingface.co/Lightricks/Wan2.2-T2V-A14B"
            },
            {
                "name": "HunyuanVideo",
                "parameters": "13B+",
                "features": "Temporal consistency, realistic",
                "license": "Apache 2.0",
                "url": "https://github.com/Tencent/HunyuanVideo"
            },
            {
                "name": "LongCat Video",
                "parameters": "13.6B",
                "features": "Minutes-long videos, 720p/30fps",
                "license": "MIT",
                "url": "https://github.com/xxlong0/LongCat"
            },
            {
                "name": "Mochi 1",
                "parameters": "10B+",
                "features": "Easy deployment",
                "license": "MIT",
                "url": "https://www.genmo.ai/mochi"
            },
            {
                "name": "ByteDance Vidi2",
                "parameters": "12B",
                "features": "Precise object editing",
                "license": "Open",
                "url": "https://winbuzzer.com"
            }
        ],
        "note": "Video generation requires significant GPU resources (A100/H100 recommended)",
        "requirements": {
            "gpu_memory": "24GB+ VRAM",
            "recommended_gpu": ["A100", "H100", "4090"],
            "deployment": "Docker + CUDA 11.8+"
        }
    }

@router.get("/health")
async def health_check():
    """Check if Video service is available"""
    return {
        "status": "placeholder",
        "service": "Video Generation",
        "message": "Video generation service requires GPU infrastructure setup"
    }
