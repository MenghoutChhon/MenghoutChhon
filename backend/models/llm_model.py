"""
Khmer LLM Model
Using PrahokBART and mT5 for text summarization and generation
"""
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class KhmerLLM:
    def __init__(self):
        """Initialize Khmer LLM models for summarization and generation"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading LLM models on {self.device}...")
        
        try:
            # Load summarization model (mT5)
            self.summarization_tokenizer = AutoTokenizer.from_pretrained(
                "google/mt5-base"
            )
            self.summarization_model = AutoModelForSeq2SeqLM.from_pretrained(
                "google/mt5-base"
            ).to(self.device)
            print("Summarization model loaded successfully")
            
            # For production, use fine-tuned Khmer models when available
            # Example: "khmer-mt5-summarization" (if published on HuggingFace)
            
        except Exception as e:
            print(f"Error loading LLM models: {e}")
            raise
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 50):
        """
        Summarize Khmer text
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
        
        Returns:
            Summarized text
        """
        try:
            # Prepare input
            inputs = self.summarization_tokenizer(
                "summarize: " + text,
                max_length=512,
                truncation=True,
                return_tensors="pt"
            ).to(self.device)
            
            # Generate summary
            with torch.no_grad():
                summary_ids = self.summarization_model.generate(
                    inputs.input_ids,
                    max_length=max_length,
                    min_length=min_length,
                    length_penalty=2.0,
                    num_beams=4,
                    early_stopping=True
                )
            
            # Decode summary
            summary = self.summarization_tokenizer.decode(
                summary_ids[0],
                skip_special_tokens=True
            )
            
            return summary
            
        except Exception as e:
            raise Exception(f"Summarization error: {str(e)}")
    
    def generate(self, prompt: str, max_length: int = 200, temperature: float = 0.7):
        """
        Generate text based on prompt
        
        Args:
            prompt: Input prompt
            max_length: Maximum length of generated text
            temperature: Sampling temperature (higher = more creative)
        
        Returns:
            Generated text
        """
        try:
            # Prepare input
            inputs = self.summarization_tokenizer(
                prompt,
                max_length=512,
                truncation=True,
                return_tensors="pt"
            ).to(self.device)
            
            # Generate text
            with torch.no_grad():
                output_ids = self.summarization_model.generate(
                    inputs.input_ids,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    num_return_sequences=1
                )
            
            # Decode output
            generated_text = self.summarization_tokenizer.decode(
                output_ids[0],
                skip_special_tokens=True
            )
            
            return generated_text
            
        except Exception as e:
            raise Exception(f"Text generation error: {str(e)}")
