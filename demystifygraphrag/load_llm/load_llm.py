from demystifygraphrag.llm.gemma2_gguf import Gemma2GGUF
from demystifygraphrag.typing import LlmLoadingConfig

def load_gemma2_gguf(config: LlmLoadingConfig) -> Gemma2GGUF:
    return Gemma2GGUF(model_path=config.model_path, tokenizer_URI=config.tokenizer_URI, context_size=config.context_size)
    

def load_gemma2_huggingface():
    pass


def load_openAI():
    pass
