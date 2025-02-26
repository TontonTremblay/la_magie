"""
llmlite - A lightweight wrapper for LLM API calls
"""

import os
import json
from typing import Dict, Any, Optional, List, Union
import openai

class LLM:
    """
    A simple wrapper for making LLM API calls
    """
    
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        """
        Initialize the LLM client
        
        Args:
            model: The model to use for generation
            api_key: OpenAI API key (if None, will try to use environment variable)
        """
        self.model = model
        
        # Set API key
        if api_key:
            openai.api_key = api_key
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
            
        if not openai.api_key:
            raise ValueError("API key must be provided either through the constructor or as an environment variable")
    
    def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text using the LLM
        
        Args:
            prompt: The prompt to send to the LLM
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (higher = more random)
            
        Returns:
            Generated text as a string
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for a text-based adventure game."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract the generated text from the response
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""
    
    def generate_json(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate JSON using the LLM
        
        Args:
            prompt: The prompt to send to the LLM
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (higher = more random)
            
        Returns:
            Generated JSON as a dictionary
        """
        # Add explicit instructions to return valid JSON
        json_prompt = f"{prompt}\n\nRespond with valid JSON only, no additional text."
        
        try:
            response_text = self.generate(json_prompt, max_tokens, temperature)
            
            # Try to parse the response as JSON
            return json.loads(response_text)
            
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the response
            try:
                # Look for JSON-like content between curly braces
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response_text[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    return {}
                    
            except Exception:
                return {} 