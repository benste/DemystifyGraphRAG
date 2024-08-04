from pydantic import BaseModel

class ChatNames(BaseModel):
    user: str = "user"
    model: str = "assistant"