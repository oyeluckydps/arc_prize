from typing import Dict, List, Callable
from pathlib import Path

import google.generativeai as genai
from .dspy_LMs.google_chat import GoogleChat
import dspy


from .llm_connector import LLMConnector


class DSPy(LLMConnector):
    '''
    WE have formed a wrapper over the DSPy library for connection with the outside world as DSPy is very young and may not be the best choice for the future.
    Essentially, we have provided four functions here:
    - one_shot: This function is same as Predict/TypedPredict of DSPy. It takes a message and returns a response in mentioned format.
    - direct: This function calls the underlying model directly. Note that it bypasses the DSPy module and does not keep the history of the conversation.
    - chat: This function calls the underlying model in chat mode. Note that it bypasses the DSPy module but keeps the history of the conversation.
    '''
    def __init__(self, strategy_method: str, system_info: str = "", model = None, chat_model = None, module = None, chat_module = None, io_signature = None) -> None:
        super().__init__(strategy_method, system_info)
        
        self.initialize_dspy(model, module, io_signature)
        self.initialize_dspy_chat(chat_model, chat_module, io_signature)
        # self.initialize_one_shot_chat()


    def initialize_dspy(self, model = None, module = None, io_signature = None) -> None: 
        import os
        # Configuring the DSPy model
        if model is None:
            self.model = dspy.Google("models/gemini-1.5-pro", api_key=os.environ['GEMINI_API_KEY'])
        else:
            self.model = model      # dspy.MODEL type model that supports calling 
        
        # Configuring the DSPy signature.
        if io_signature is None:
            self.io_signature = 'question -> answer'
        else:
            self.io_signature = io_signature
        
        # Configuring the DSPy one_shot module.
        if module is None and io_signature is None:
            self._one_shot_module = dspy.Predict(signature = self.io_signature)
        elif module is None and io_signature is not None:
            self._one_shot_module = dspy.TypedPredictor(signature = self.io_signature)
        else:
            self._one_shot_module = module
            self._one_shot_module.signature = self.io_signature
            # self._one_shot_module.lm = self.model

    def initialize_dspy_chat(self, chat_model = None, chat_module = None, io_signature = None) -> None: 
        import os
        # Configuring the DSPy chat model
        if chat_model is None:
            self.chat_model = GoogleChat("models/gemini-1.5-pro", api_key=os.environ['GEMINI_API_KEY'])
        else:
            self.chat_model = chat_model      # dspy.MODEL type model that supports calling 
        
        # Configuring the DSPy signature.
        if io_signature is None:
            self.io_signature = 'question -> answer'
        else:
            self.io_signature = io_signature
        
        # Configuring the DSPy chat module.
        if chat_module is None and io_signature is None:
            self._chat_module = dspy.Predict(signature = self.io_signature, lm=self.chat_model)
        elif chat_module is None and io_signature is not None:
            self._chat_module = dspy.TypedPredictor(signature = self.io_signature)
        else:
            self._chat_module = chat_module
            self._chat_module.signature = self.io_signature
            self._chat_module.lm = self.chat_model


    def one_shot(self, *args, **kwargs):
        saved_config = dspy.settings.config
        dspy.settings.configure(lm=self.model, max_tokens=8196)
        response = self._one_shot_module(*args, **kwargs)  # I have to mention it again due to a bug in the DSPy library. It either takes the glovally set LM or locally passed and not the LM set in Predict/TypedPredict.
        dspy.settings.configure(**saved_config)
        return response

    def chat(self, *args, **kwargs) -> str:
        all_responses = []
        saved_config = dspy.settings.config
        dspy.settings.configure(lm=self.chat_model, max_tokens=8196)
        if len(args) > 0:
            for arg in args:
                all_responses.append(self._chat_module.config["lm"].basic_request(arg))
        if len(kwargs) > 0:
            all_responses.append(self._chat_module(**kwargs))
        dspy.settings.configure(**saved_config)
        return all_responses if len(all_responses)>1 else all_responses[0]
    
    def chat_history(self) -> str:
        return self._chat_module.lm.history()
    
    def clear_chat(self) -> None:
        self._chat_module.lm.history = []

