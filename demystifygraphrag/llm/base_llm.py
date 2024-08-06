from typing import List, Iterator
from datetime import datetime
from copy import deepcopy

from .typing import ChatNames
    
class LLM:
    model = None
    tokenizer = None
    chatnames: ChatNames = ChatNames()
    
    def format_chat(self, chat: List[tuple], established_chat: List[dict] = []) -> List[dict]:
        """format chat with the correct names ready for `tokenizer.apply_chat_template`

        Args:
            chat (List[tuple]): [(role: content), (role: content)]
                                role (str): either "user" or "model"
                                content (str)
            established_chat (List[dict], optional): Already established chat to append to. Defaults to [].

        Returns:
            List[dict]: _description_
        """
        
        # Make sure we don't change the input variable
        formatted_chat = deepcopy(established_chat)
        
        for role, content in chat:
            formatted_chat.append({"role": self.chatnames.model_dump()[role], "content": content})
            
        return formatted_chat
    
    def run_chat(self, chat: List[dict], stream: bool = False) -> str:
        pass
    
    def tokenize(self, content: str) -> List[str]:
        pass
    
    def untokenize(self, tokens: List[str]) -> str:
        pass
    
    def print_streamed(self, stream: Iterator, timeit: bool = False) -> str:
        full_text = ""
        start = datetime.now()
        num_tokens = 0
        for s in stream:
            token = s["choices"][0]["text"]
            print(token, end="", flush=True)
            full_text += token
            num_tokens += 1
            
        elapsed_time = datetime.now()-start
        if timeit:
            print(f"tokens / sec = {num_tokens / elapsed_time.seconds}")

        return full_text