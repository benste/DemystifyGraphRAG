import html
import re
from typing import Any, Iterator
from datetime import datetime

from llama_cpp import CreateCompletionResponse

def print_streamed(stream: Iterator[CreateCompletionResponse], timeit: bool = False) -> str:
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

def clean_str(input: Any) -> str:
    """Clean an input string by removing HTML escapes, control characters, and other unwanted characters."""
    # If we get non-string input, just give it back
    if not isinstance(input, str):
        return input

    result = html.unescape(input.strip())
    result = result.lstrip('"').rstrip('"')
    # https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python
    return re.sub(r"[\x00-\x1f\x7f-\x9f]", "", result)
