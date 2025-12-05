"""
Configuration module for the Khmer AI/ML Platform
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    api_title: str = "Khmer AI/ML Platform API"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS Settings
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Model Settings
    tts_model: str = "facebook/mms-tts-khm"
    ocr_model: str = "songhieng/khmer-trocr-ocr-v1.0"
    summarization_model: str = "Seanghay/khmer-mt5-summarization"
    
    # GPU Settings
    cuda_visible_devices: str = "0"
    
    # Cache Settings
    model_cache_dir: str = "/root/.cache/huggingface"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
