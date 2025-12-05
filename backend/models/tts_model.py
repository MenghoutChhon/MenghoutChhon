"""
Khmer Text-to-Speech Model
Using Meta's Massively Multilingual Speech (MMS) for Khmer
Model: facebook/mms-tts-khm
"""
import torch
import numpy as np
from transformers import VitsModel, AutoTokenizer
import io
import soundfile as sf

class KhmerTTS:
    def __init__(self, model_name="facebook/mms-tts-khm"):
        """
        Initialize Khmer TTS model
        
        Args:
            model_name: HuggingFace model identifier
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading TTS model on {self.device}...")
        
        try:
            self.model = VitsModel.from_pretrained(model_name).to(self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            print(f"TTS model {model_name} loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def synthesize(self, text: str, speed: float = 1.0):
        """
        Convert text to speech
        
        Args:
            text: Khmer text to synthesize
            speed: Speech speed multiplier (1.0 = normal)
        
        Returns:
            Tuple of (audio_bytes, duration)
        """
        try:
            # Tokenize input text
            inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
            
            # Generate speech
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Get waveform
            waveform = outputs.waveform[0].cpu().numpy()
            
            # Adjust speed if needed
            if speed != 1.0:
                waveform = self._adjust_speed(waveform, speed)
            
            # Convert to bytes
            audio_bytes = self._waveform_to_bytes(waveform)
            
            # Calculate duration
            sample_rate = self.model.config.sampling_rate
            duration = len(waveform) / sample_rate
            
            return audio_bytes, duration
            
        except Exception as e:
            raise Exception(f"TTS synthesis error: {str(e)}")
    
    def _adjust_speed(self, waveform, speed):
        """Adjust audio speed"""
        # Simple speed adjustment by resampling
        # For production, use librosa or similar for better quality
        indices = np.arange(0, len(waveform), speed)
        indices = indices[indices < len(waveform)].astype(int)
        return waveform[indices]
    
    def _waveform_to_bytes(self, waveform):
        """Convert waveform to audio bytes (WAV format)"""
        buffer = io.BytesIO()
        sample_rate = self.model.config.sampling_rate
        sf.write(buffer, waveform, sample_rate, format='WAV')
        buffer.seek(0)
        return buffer.read()
