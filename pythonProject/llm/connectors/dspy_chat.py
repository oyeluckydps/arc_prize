from typing import Dict, List, Callable
from pathlib import Path

import google.generativeai as genai
import dspy


from .llm_connector import LLMConnector
from .dspy_LMs.custom_google import CustomGoogle


class DSPyChat(LLMConnector):
    '''
    We have formed a wrapper over the DSPy library for connection with theoutside world as DSPy is very young and may not be the best choice for the future.
    This time we have implemented a custom LM using the Gemini model as we needed a chat session, while the DSPy module only provides the Generative model and not chat session by default.
    Essentially, we have provided one function only:
    - dspy_chat: This function is same as Predict/TypedPredict of DSPy but it keeps the history of the conversation. Be mindful to not let it grow too long as it sends the complete history to the LLM everytime.
    '''
    def __init__(self, strategy_method: str = '', system_info: str = "", module = None, model = None, io_signature = None) -> None:
        super().__init__(strategy_method, system_info)
        self.initialize_dspy_chat(module, model, io_signature)


    def initialize_dspy_chat(self, module = None, model = None, io_signature = None) -> None:
        # Configuring the DSPy model
        if model is None:
            # Getting the API key.
            gemini_key_path = Path(".gemini_key")
            with gemini_key_path.open('r') as file:
                gemini_key = file.read()
            self.model = CustomGoogle("models/gemini-1.5-pro", api_key=gemini_key)
        else:
            self.model = model      # dspy.MODEL type model
        dspy.settings.configure(lm=self.model, max_tokens=65536)
        
        self.__direct_chat = self.model.llm.send_message 

        # Configuring the DSPy IO signature
        if io_signature is None and module is None:
            self.io_signature = 'question -> answer'
            self.module = dspy.Predict(self.io_signature)
        elif io_signature is not None and module is None:
            self.io_signature = io_signature
            self.module = dspy.TypedPredictor(self.io_signature)
        elif io_signature is None and module is not None:
            self.module = module       # This is typical use case where configured module is passed.
        else:                          # Module is passed but IO signature is not configured in the module. We need to reconfigure the module.
            self.io_signature = io_signature
            self.module = dspy.Predict(self.io_signature)

        # print(f"Initialized DSPy LLM with model {self.model} \n Module = {self.module} \n and io_signature = {self.io_signature}")

    def history(self):
        return self.model.llm.history()
    
    def clear_history(self):
        self.model.llm.history = []

    def send_message(self, *args, **kwargs):        
        if len(args) > 0:
            response = self.direct_chat(*args).text            # Direct call to the LLM with passed prompts.
            self.chat_history.append({"role": "user", "content": args})
            self.chat_history.append({"role": "assistant", "content": response})
        if len(kwargs) > 0:
            response2 = self.dspy_chat(**kwargs)               # Call through DSPy to the LLM with passed singature template based prompt.
            self.chat_history.append({"role": "user", "content": kwargs})
            self.chat_history.append({"role": "assistant", "content": response2})
            return response2    # If you want both the responses, you should call with args only first and then with kwargs only i.e. with signature template vased primpt.
        return response


    def dspy_chat(self, **kwargs):
        response = self.module(**kwargs)                # Call the module with the kwargs.
        return response
    

    def direct_chat(self, *args):
        response = self.__direct_chat(list(args))       # Direct call to the LLM with passed prompts.
        return response


    def one_shot(self, message: str) -> str:
        raise NotImplementedError("DSPy Chat's one_shot strategy not provided")


    def chain_of_thought(self, message: str) -> str:
        raise NotImplementedError("DSPy's CoT strategy not provided")


    def loop(self, message: str) -> str:
        raise NotImplementedError("DSPy's loop strategy not provided")

