
from copy import deepcopy
from postprocessing.utils import print_streamed

def run_chat(chat: list, configured_llm: dict, completion_delimiter: str = ""):
    llm_input = configured_llm["tokenizer"].apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
    llm_stream = configured_llm["llm"](llm_input, max_tokens=-1, stop=["<eos>"], echo=False, stream=True)
    return print_streamed(llm_stream).removesuffix(completion_delimiter)
    
def loop_extraction(documents: dict[int: str], formatting: dict, configured_llm: dict, max_gleans: int = 5):
    completion_delimiter = formatting['completion_delimiter']
    
    llm_raw_output = {}
    for source_doc_id, doc in documents.items():
        print(f"\n-->processing chunk {len(llm_raw_output)+1} of {len(documents)}")
        formatting['input_text'] = doc
    
        prompt = formatting['default_prompt'].format(**formatting)
        chat = [
            {
                "role": configured_llm["chatnames"]["user"],
                "content": prompt,
            }
        ]
        raw_output = run_chat(chat, configured_llm, completion_delimiter)
        llm_raw_output[source_doc_id] = raw_output
        
        # Add entities LLM might have missed first time around
        for g in range(max_gleans):
            print(f"\n-->trying to get more entities out of chunk ({g+1} / max {max_gleans})")
            chat.append(
                {
                    "role": configured_llm["chatnames"]["model"],
                    "content": raw_output,
                }
            )
            chat.append(
                {
                    "role": configured_llm["chatnames"]["user"],
                    "content": formatting['continue_prompt'],
                }
            )
            raw_output = run_chat(chat, configured_llm, completion_delimiter)
            llm_raw_output[source_doc_id] += formatting['record_delimiter'] + raw_output or ""

            # Check if the LLM thinks there are still entities missing
            loop_chat = deepcopy(chat)
            loop_chat.append(
                {
                    "role": configured_llm["chatnames"]["model"],
                    "content": llm_raw_output[source_doc_id],
                },
            )
            loop_chat.append(
                {
                    "role": configured_llm["chatnames"]["user"],
                    "content": formatting['loop_prompt'],
                }
            )
            continuation = run_chat(loop_chat, configured_llm, completion_delimiter)
            if continuation.lower() != "yes" or continuation.lower() == "no":
                break
                
    return llm_raw_output
