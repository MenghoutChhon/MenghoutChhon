"""
Video Generation API Router
Using Mochi 1 or Wan2.2 for text-to-video generation
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import uuid
from models.video_model import VideoGenerator

router = APIRouter()
video_model = None

# Store for video generation jobs
video_jobs = {}

class VideoRequest(BaseModel):
    prompt: str
    duration: Optional[int] = 5  # seconds
    resolution: Optional[str] = "720p"
    fps: Optional[int] = 30

class VideoResponse(BaseModel):
    job_id: str
    status: str
    message: str

class VideoStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: Optional[int] = None
    video_url: Optional[str] = None
    error: Optional[str] = None

@router.on_event("startup")
async def load_model():
    """Load video generation model on startup"""
    global video_model
    try:
        video_model = VideoGenerator()
        print("Video generation model loaded successfully")
    except Exception as e:
        print(f"Error loading video generation model: {e}")

@router.post("/generate", response_model=VideoResponse)
async def generate_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """
    Generate video from text prompt
    
    Args:
        request: VideoRequest with prompt and video parameters
    
    Returns:
        Job ID for tracking video generation progress
    """
    if not video_model:
        raise HTTPException(status_code=503, detail="Video generation model not loaded")
    
    # Create job ID
    job_id = str(uuid.uuid4())
    video_jobs[job_id] = {
        "status": "queued",
        "progress": 0
    }
    
    # Add video generation to background tasks
    background_tasks.add_task(
        generate_video_task,
        job_id=job_id,
        prompt=request.prompt,
        duration=request.duration,
        resolution=request.resolution,
        fps=request.fps
    )
    
    return VideoResponse(
        job_id=job_id,
        status="queued",
        message="Video generation started. Use /status/{job_id} to check progress."
    )

async def generate_video_task(job_id: str, prompt: str, duration: int, resolution: str, fps: int):
    """Background task for video generation"""
    try:
        video_jobs[job_id]["status"] = "processing"
        
        # Generate video
        video_path = video_model.generate(
            prompt=prompt,
            duration=duration,
            resolution=resolution,
            fps=fps,
            progress_callback=lambda p: video_jobs[job_id].update({"progress": p})
        )
        
        video_jobs[job_id].update({
            "status": "completed",
            "progress": 100,
            "video_url": f"/api/video/download/{job_id}"
        })
    except Exception as e:
        video_jobs[job_id].update({
            "status": "failed",
            "error": str(e)
        })

@router.get("/status/{job_id}", response_model=VideoStatusResponse)
async def get_video_status(job_id: str):
    """
    Get status of video generation job
    
    Args:
        job_id: Job ID returned from generate endpoint
    
    Returns:
        Current status of video generation
    """
    if job_id not in video_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = video_jobs[job_id]
    return VideoStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job.get("progress"),
        video_url=job.get("video_url"),
        error=job.get("error")
    )

@router.get("/models")
async def get_status():
    """Get video generation model status"""
    return {
        "model_loaded": video_model is not None,
        "available_models": ["Mochi 1", "Wan2.2"] if video_model else None,
        "supported_resolutions": ["720p", "1080p"],
        "max_duration": 10  # seconds
    }
