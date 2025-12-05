"""
FastAPI Backend for Khmer AI/ML Platform
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import tts_router, ocr_router, llm_router, video_router

app = FastAPI(
    title="Khmer AI/ML Platform API",
    description="AI/ML services for Khmer language including TTS, OCR, Summarization, and Video Generation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tts_router.router, prefix="/api/tts", tags=["Text-to-Speech"])
app.include_router(ocr_router.router, prefix="/api/ocr", tags=["OCR"])
app.include_router(llm_router.router, prefix="/api/llm", tags=["Language Models"])
app.include_router(video_router.router, prefix="/api/video", tags=["Video Generation"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Khmer AI/ML Platform API",
        "version": "1.0.0",
        "endpoints": {
            "tts": "/api/tts",
            "ocr": "/api/ocr",
            "llm": "/api/llm",
            "video": "/api/video",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
