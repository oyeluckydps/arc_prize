from typing import Dict, List, Callable
from .llm_connector import LLMConnector

import google.generativeai as genai

class Gemini(LLMConnector):
    def __init__(self, strategy_method: str, system_info: str = "", model: genai.ChatSession = None) -> None:
        super().__init__(strategy_method, system_info)
        if model is not None:
            self.model = model
            if system_info != "":
                self.model.system_instruction = system_info
        else:
            self.initialize_gemini()


    def initialize_gemini(self) -> None:
        from pathlib import Path

        # Getting the API key.
        gemini_key_path = Path(".gemini_key")
        with gemini_key_path.open('r') as file:
            gemini_key = file.read()
        genai.configure(api_key=gemini_key)

        # Config for Gemini LLM initialization
        generation_config = {
                          "temperature": 1,
                          "top_p": 0.95,
                          "top_k": 64,
                          "max_output_tokens": 8192,
                          "response_mime_type": "text/plain",
                        }
    
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=self.system_info)
        
        self.model = model.start_chat()

        print("Initialized Gemini LLM")


    def zero_shot(self, message: str) -> str:
        response = self.model.send_message(message)
        return response.text


    def chain_of_thought(self, message: str) -> str:
        raise NotImplementedError("Gemini's CoT strategy not provided")


    def loop(self, message: str) -> str:
        raise NotImplementedError("Gemini's loop strategy not provided")
    
    