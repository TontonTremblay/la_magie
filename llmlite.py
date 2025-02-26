"""
llmlite - A lightweight wrapper for LLM API calls
"""

import os
import json
import tempfile
import subprocess
from typing import Dict, Any, Optional, List, Union
import openai

class LLM:
    """
    A simple wrapper for making LLM API calls
    """
    
    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None):
        """
        Initialize the LLM client
        
        Args:
            model: The model to use for generation (default is now gpt-4o)
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
    
    def text_to_speech(self, text: str, voice: str = "onyx") -> bool:
        """
        Convert text to speech using OpenAI's TTS API
        
        Args:
            text: The text to convert to speech
            voice: The voice to use (default is "onyx")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a temporary file to store the audio
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Generate speech using OpenAI's API
            response = openai.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            # Save the audio to the temporary file
            response.stream_to_file(temp_path)
            
            # Play the audio using the appropriate command based on the OS
            if os.name == 'nt':  # Windows
                os.startfile(temp_path)
            elif os.name == 'posix':  # macOS or Linux
                if subprocess.call(['which', 'afplay'], stdout=subprocess.DEVNULL) == 0:  # macOS
                    subprocess.Popen(['afplay', temp_path])
                elif subprocess.call(['which', 'mpg123'], stdout=subprocess.DEVNULL) == 0:  # Linux with mpg123
                    subprocess.Popen(['mpg123', temp_path])
                elif subprocess.call(['which', 'mpg321'], stdout=subprocess.DEVNULL) == 0:  # Linux with mpg321
                    subprocess.Popen(['mpg321', temp_path])
                else:
                    print("Could not find a suitable audio player. Please install mpg123 or mpg321.")
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error generating speech: {e}")
            return False 