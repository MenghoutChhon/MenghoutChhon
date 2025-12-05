"""
TTS (Text-to-Speech) Model Handler
Uses Meta's MMS-TTS for Khmer language
"""
from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile as wavfile
import numpy as np
from pathlib import Path

class TTSModel:
    def __init__(self):
        self.model_name = "facebook/mms-tts-khm"
        self.model = None
        self.tokenizer = None
        self.sample_rate = 16000
        
    def load_model(self):
        """Load the TTS model and tokenizer"""
        if self.model is None:
            print(f"Loading TTS model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = VitsModel.from_pretrained(self.model_name)
            print("TTS model loaded successfully")
    
    def generate_speech(self, text: str, output_path: str = None) -> dict:
        """
        Generate speech from Khmer text
        
        Args:
            text: Khmer text to convert to speech
            output_path: Optional path to save the audio file
            
        Returns:
            dict with audio data and metadata
        """
        self.load_model()
        
        # Tokenize input
        inputs = self.tokenizer(text, return_tensors="pt")
        
        # Generate speech
        with torch.no_grad():
            output = self.model(**inputs).waveform
        
        # Convert to numpy array
        audio_data = output.squeeze().cpu().numpy()
        
        # Save to file if path provided
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            wavfile.write(output_path, self.sample_rate, audio_data)
        
        return {
            "audio_data": audio_data.tolist(),
            "sample_rate": self.sample_rate,
            "duration": len(audio_data) / self.sample_rate,
            "text": text
        }

# Global instance
tts_model = TTSModel()
