"""
Khmer OCR Model
Using TrOCR fine-tuned for Khmer text recognition
Model: songhieng/khmer-trocr-ocr-v1.0
"""
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import io

class KhmerOCR:
    def __init__(self, model_name="songhieng/khmer-trocr-ocr-v1.0"):
        """
        Initialize Khmer OCR model
        
        Args:
            model_name: HuggingFace model identifier
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading OCR model on {self.device}...")
        
        try:
            self.processor = TrOCRProcessor.from_pretrained(model_name)
            self.model = VisionEncoderDecoderModel.from_pretrained(model_name).to(self.device)
            print(f"OCR model {model_name} loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback to base TrOCR model
            print("Attempting to load base TrOCR model...")
            self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
            self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten").to(self.device)
    
    def recognize(self, image_data: bytes):
        """
        Perform OCR on image
        
        Args:
            image_data: Image bytes
        
        Returns:
            Dictionary with recognized text, confidence, and lines
        """
        try:
            # Load image
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            
            # Process image
            pixel_values = self.processor(image, return_tensors="pt").pixel_values.to(self.device)
            
            # Generate text
            with torch.no_grad():
                generated_ids = self.model.generate(pixel_values)
            
            # Decode
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # Split into lines (simple approach)
            lines = [line.strip() for line in generated_text.split('\n') if line.strip()]
            
            # Calculate approximate confidence (simplified)
            # In production, use model's output probabilities
            confidence = 0.85  # Placeholder
            
            return {
                'text': generated_text,
                'confidence': confidence,
                'lines': lines if lines else [generated_text]
            }
            
        except Exception as e:
            raise Exception(f"OCR recognition error: {str(e)}")
    
    def recognize_batch(self, image_data_list):
        """
        Perform OCR on multiple images
        
        Args:
            image_data_list: List of image bytes
        
        Returns:
            List of recognition results
        """
        results = []
        for image_data in image_data_list:
            results.append(self.recognize(image_data))
        return results
