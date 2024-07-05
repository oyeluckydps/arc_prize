from typing import Dict, List, Callable
from .llm_connector import LLMConnector

import google.generativeai as genai

class Gemini(LLMConnector):
    def __init__(self, strategy_method: str, system_info: str = "", model: genai.GenerativeModel = None) -> None:
        super().__init__(strategy_method, system_info)
        self.initialize_gemini(model)


    def initialize_gemini(self, model: genai.GenerativeModel = None) -> None:
        from pathlib import Path
        import os

        # Getting the API key.
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        if model is None:
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
        
        self.direct_model = model
        self.chat_model = model.start_chat()

        print("Initialized Gemini LLM")

    def chat_history(self, message: str) -> str:
        return self.chat_model.history

    def clear_chat(self, message: str) -> str:
        self.chat_model.history = []

    def one_shot(self, message: str) -> str:
        response = self.model.generate_content(message)
        return response.text


    def chat(self, message: str) -> str:
        response = self.chat_model.send_message(message)
        return response.text


