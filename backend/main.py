"""
LMN - Khmer AI/ML Platform
Main FastAPI Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import tts_router, ocr_router, llm_router, video_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load models
    await tts_router.load_model()
    await ocr_router.load_model()
    await llm_router.load_model()
    await video_router.load_model()
    yield
    # Shutdown: Cleanup if needed

app = FastAPI(
    title="LMN - Khmer AI/ML Platform",
    description="Comprehensive AI/ML platform for Khmer language processing",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tts_router.router, prefix="/api/tts", tags=["Text-to-Speech"])
app.include_router(ocr_router.router, prefix="/api/ocr", tags=["OCR"])
app.include_router(llm_router.router, prefix="/api/llm", tags=["LLM"])
app.include_router(video_router.router, prefix="/api/video", tags=["Video Generation"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to LMN - Khmer AI/ML Platform",
        "version": "1.0.0",
        "endpoints": {
            "tts": "/api/tts",
            "ocr": "/api/ocr",
            "llm": "/api/llm",
            "video": "/api/video"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
