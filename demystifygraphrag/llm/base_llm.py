from typing import List, Iterator
from datetime import datetime

from .typing import ChatNames
    
class LLM:
    model = None
    tokenizer = None
    chatnames: ChatNames = ChatNames()
    
    def run_chat(self, chat: List[dict]):
        pass
    
    def tokenize(self, content: str):
        pass
    
    def untokenize(self, tokens: List[str]):
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