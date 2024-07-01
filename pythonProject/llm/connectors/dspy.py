from typing import Dict, List, Callable
from pathlib import Path

import google.generativeai as genai
import dspy


from .llm_connector import LLMConnector


class DSPy(LLMConnector):
    '''
    WE have formed a wrapper over the DSPy library for connection with theoutside world as DSPy is very young and may not be the best choice for the future.
    Essentially, we have provided four functions here:
    - one_shot: This function is same as Predict/TypedPredict of DSPy. It takes a message and returns a response in mentioned format.
    - direct: This function calls the underlying modeel directly. Note that it bypasses the DSPy module and does not keep the history of the conversation.
    - chat: This function calls the underlying model in chat mode. Note that it bypasses the DSPy module but keeps the history of the conversation.
    '''
    def __init__(self, strategy_method: str, system_info: str = "", module = None, model = None, io_signature = None) -> None:
        super().__init__(strategy_method, system_info)
        
        if strategy_method is None and io_signature is None:
            self.current_strategy = self.direct
        elif strategy_method == 'direct':
            self.current_strategy = self.direct
        elif strategy_method == 'chat':
            self.current_strategy = self.chat
        # Else if strategy_method is None but io_signature is not None then current_strategy is already assigned the zero_shot method.
        
        self.initialize_dspy(module, model, io_signature)
        # self.initialize_one_shot_chat()


    def initialize_dspy(self, module = None, model = None, io_signature = None) -> None:
        # Configuring the DSPy model
        if model is None:
            # Getting the API key.
            gemini_key_path = Path(".gemini_key")
            with gemini_key_path.open('r') as file:
                gemini_key = file.read()
            self.model = dspy.Google("models/gemini-1.5-pro", api_key=gemini_key)
        else:
            self.model = model      # dspy.MODEL type model
        dspy.settings.configure(lm=self.model, max_tokens=8196)
        
        self.__direct_call = self.model.basic_request               # Use it to send direct message to the model (any model) bypassing the DSPy module.

        # Chat with history only supported for Gemini models as of now.
        # Configure the chat (with history) methods. Unfortuantely, it is not possible to use the benefits of DSPy with the chat with history method.
        if isinstance(dspy.settings.config["lm"].llm, genai.GenerativeModel):
            self.__chat_session = dspy.settings.config["lm"].llm.start_chat()           # Start a new chat session. You may use this to check the status of the chat session.
            self.__chat = self.__chat_session.send_message                              # Send a message through the chat session.

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


    def send_message(self, *args, **kwargs):
        response = self.current_strategy(*args, **kwargs)       # Configured by default to direct if strategy_method is None and io_signature is None, else zero_shot if strategy_method wass None at initialization.
        self.chat_history.append({"role": "user", "content": (args, kwargs)})
        self.chat_history.append({"role": "assistant", "content": response})
        return response
    

    def one_shot(self, *args,**kwargs):
        response = self.module(*args, **kwargs)
        return response


    def chain_of_thought(self, message: str) -> str:
        raise NotImplementedError("DSPy's CoT strategy not provided")


    def loop(self, message: str) -> str:
        raise NotImplementedError("DSPy's loop strategy not provided")


    def direct(self, message: str) -> str:
        response = self.__direct_call(message)
        return response.text


    def chat(self, message: str) -> str:
        response = self.__chat(message)
        return response.text
    
