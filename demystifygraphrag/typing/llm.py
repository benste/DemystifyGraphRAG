from pydantic import BaseModel

class LlmLoadingParams(BaseModel):
    """Params for loading local LLM"""

    model_path: str
    tokenizer_URI: str

