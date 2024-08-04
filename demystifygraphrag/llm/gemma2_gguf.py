from typing import List

from llama_cpp import Llama
from transformers import AutoTokenizer

from demystifygraphrag.llm.base_llm import LLM, ChatNames

class Gemma2GGUF(LLM):
    
    def __init__(self, model_path: str, tokenizer_URI: str, context_size: int = 8192):
        self.model = Llama(model_path=model_path, verbose=False, n_ctx=context_size)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_URI)
        self.chatnames = ChatNames(user = 'user', model = 'tokenizer')

    def run_chat(self, chat: List[dict], stream: bool = False) -> str:
        llm_input = self.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
        results = self.model(llm_input, max_tokens=-1, stop=["<eos>"], echo=False, stream=stream)
        if stream:
            results = self.print_streamed(results)
            
        return results
        
    def tokenize(self, content: str) -> List[str]:
        return self.tokenizer.tokenize(content)
    
    def untokenize(self, tokens: List[str]):
        return self.tokenizer.convert_tokens_to_string(tokens)
    

