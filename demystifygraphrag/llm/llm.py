from typing import Any, List

from dagster import op, Config

class LLMHelper:
    def __init__(self):
        self.llm = None
        self.tokenizer = None
        
    def tokenize(self, content: str):
        pass
    
    def run_chat(self, chat: List[dict]):
        pass
        
class LLM(Config):
    llm: LLMHelper
    tokenizer: Any
    
@op
def llm(loaded_llm: LLM) -> LLM:
    return loaded_llm