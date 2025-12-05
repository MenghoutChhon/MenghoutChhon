"""
OCR (Optical Character Recognition) Model Handler
Uses TrOCR fine-tuned for Khmer language
"""
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

class OCRModel:
    def __init__(self):
        self.model_name = "songhieng/khmer-trocr-ocr-v1.0"
        self.model = None
        self.processor = None
        
    def load_model(self):
        """Load the OCR model and processor"""
        if self.model is None:
            print(f"Loading OCR model: {self.model_name}")
            self.processor = TrOCRProcessor.from_pretrained(self.model_name)
            self.model = VisionEncoderDecoderModel.from_pretrained(self.model_name)
            print("OCR model loaded successfully")
    
    def extract_text(self, image_path: str = None, image_bytes: bytes = None) -> dict:
        """
        Extract Khmer text from image
        
        Args:
            image_path: Path to image file
            image_bytes: Image bytes data
            
        Returns:
            dict with extracted text and confidence
        """
        self.load_model()
        
        # Load image
        if image_path:
            image = Image.open(image_path).convert("RGB")
        elif image_bytes:
            import io
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        else:
            raise ValueError("Either image_path or image_bytes must be provided")
        
        # Process image
        pixel_values = self.processor(image, return_tensors="pt").pixel_values
        
        # Generate text
        with torch.no_grad():
            generated_ids = self.model.generate(pixel_values)
        
        # Decode text
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return {
            "text": generated_text,
            "language": "khmer",
            "model": self.model_name
        }

# Global instance
ocr_model = OCRModel()
