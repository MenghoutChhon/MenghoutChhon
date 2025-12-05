"""
Summarization and Text Generation Model Handler
Uses mT5 fine-tuned for Khmer summarization
"""
from transformers import MT5ForConditionalGeneration, MT5Tokenizer
import torch

class SummarizationModel:
    def __init__(self):
        self.model_name = "Seanghay/khmer-mt5-summarization"
        self.model = None
        self.tokenizer = None
        
    def load_model(self):
        """Load the summarization model and tokenizer"""
        if self.model is None:
            print(f"Loading Summarization model: {self.model_name}")
            self.tokenizer = MT5Tokenizer.from_pretrained(self.model_name)
            self.model = MT5ForConditionalGeneration.from_pretrained(self.model_name)
            print("Summarization model loaded successfully")
    
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 30) -> dict:
        """
        Summarize Khmer text
        
        Args:
            text: Khmer text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            dict with summary and metadata
        """
        self.load_model()
        
        # Prepare input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )
        
        # Generate summary
        with torch.no_grad():
            summary_ids = self.model.generate(
                inputs.input_ids,
                max_length=max_length,
                min_length=min_length,
                num_beams=4,
                early_stopping=True
            )
        
        # Decode summary
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        return {
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
            "model": self.model_name
        }
    
    def generate_text(self, prompt: str, max_length: int = 200) -> dict:
        """
        Generate text from prompt
        
        Args:
            prompt: Text prompt
            max_length: Maximum length of generated text
            
        Returns:
            dict with generated text
        """
        self.load_model()
        
        # Prepare input
        inputs = self.tokenizer(prompt, return_tensors="pt")
        
        # Generate text
        with torch.no_grad():
            output_ids = self.model.generate(
                inputs.input_ids,
                max_length=max_length,
                num_beams=4,
                early_stopping=True,
                temperature=0.7
            )
        
        # Decode output
        generated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        return {
            "generated_text": generated_text,
            "prompt": prompt,
            "model": self.model_name
        }

# Global instance
summarization_model = SummarizationModel()
