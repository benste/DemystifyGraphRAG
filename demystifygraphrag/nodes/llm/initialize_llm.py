from demystifygraphrag.llm.gemma2_gguf import Gemma2GGUF

def initialize_gemma2_gguf(config: dict) -> Gemma2GGUF:
    return Gemma2GGUF(model_path=config["model_path"], tokenizer_URI=config["tokenizer_URI"])
    

def initialize_gemma2_huggingface():
    pass


def initialize_openAI():
    pass
