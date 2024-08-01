from typing import List

from llama_cpp import Llama
from transformers import AutoTokenizer

from demystifygraphrag.llm.llm import LLM, LLMHelper

model_path = "/home/bens/projects/DemystifyGraphRAG/models/gemma-2-9b-it-IQ4_XS.gguf"
tokenizer_URI = "google/gemma-2-9b-it"
context_size = 8192

llm = Llama(model_path=model_path, verbose=False, n_ctx=context_size)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_URI)

class Gegmma2(LLMHelper):
    def __init__(self):
        self.llm = llm
        self.tokenizer = tokenizer
        
        if self.tokenizer.chat_template is None:
            self.chatnames = {"user": "user", "model": "assistant"}
        elif "message['role'] == 'assistant'" in self.tokenizer.chat_template:
            self.chatnames = {"user": "user", "model": "assistant"}
        else:
            self.chatnames = {"user": "user", "model": "model"}
            
    def tokenize(self, content: str):
        return self.tokenizer.tokenize(content)
    
    def run_chat(self, chat: List[dict]):
        llm_input = self.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
        return self.llm(llm_input, max_tokens=-1, stop=["<eos>"], echo=False, stream=False)
    
gemma2_instance = LLM(
    llm = Gegmma2(),
    tokenizer = tokenizer
)