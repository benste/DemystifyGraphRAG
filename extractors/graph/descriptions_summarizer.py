from typing import List
from copy import deepcopy

import networkx as nx

from default_prompts import summarize as summarize_default_prompt
from extractors.graph.utils import run_chat
from extractors.typing import SummarizationResult

# Max token size for input prompts
DEFAULT_MAX_INPUT_TOKENS = 4_000
# Max token count for LLM answers
DEFAULT_MAX_SUMMARY_LENGTH = 500

def num_tokens_from_string(
    string: str, configured_llm: dict
) -> int:
    """Return the number of tokens in a text string."""
    return len(configured_llm["tokenizer"].tokenize(string))

def description_summary_from_llm(entities: List[str], descriptions: List[str], configured_llm: dict):
    formatting = deepcopy(summarize_default_prompt.DEFAULT_FORMATTING)
    formatting["entity_names"] = entities
    formatting["description_list"] = descriptions
    
    prompt = summarize_default_prompt.SUMMARIZE_PROMPT.format(**formatting)
    chat = [
        {
            "role": configured_llm["chatnames"]["user"],
            "content": prompt,
        }
    ]
    return run_chat(chat, configured_llm)

def summarize_item(graph_item, entities, configured_llm: dict, max_input_tokens = None, max_output_tokens = None):
    max_input_tokens = max_input_tokens or DEFAULT_MAX_INPUT_TOKENS
    max_output_tokens = max_output_tokens or DEFAULT_MAX_SUMMARY_LENGTH
    
    usable_tokens = max_input_tokens - num_tokens_from_string(
            summarize_default_prompt.SUMMARIZE_PROMPT, configured_llm
        )

    descriptions_collected = []
    result = ""
    for description in entities:
        usable_tokens -= num_tokens_from_string(description, configured_llm)
        descriptions_collected.append(description)
        
        # If buffer is full, or all descriptions have been added, summarize
        if usable_tokens <= 0:
            # Calculate result (final or partial)
            result = description_summary_from_llm(graph_item, descriptions_collected, configured_llm)
            
            # reset values for a possible next loop
            descriptions_collected = [result]
            usable_tokens = (
                max_input_tokens
                - num_tokens_from_string(summarize_default_prompt.SUMMARIZE_PROMPT, configured_llm)
                - num_tokens_from_string(result, configured_llm)
            )

    if len(descriptions_collected) > 1:
        result = description_summary_from_llm(graph_item, descriptions_collected, configured_llm)
        
    return entities, result
                    

def summarize(graph: nx.classes.graph.Graph, configured_llm: dict):
    for node in graph.nodes():
        descriptions = sorted(set(graph.nodes[node].get("description", "").split("\n")))
        graph.nodes[node]["description"] = summarize_item(node, descriptions, configured_llm)
        
    for edge in graph.edges():
        descriptions = sorted(set(graph.edges[edge].get("description", "").split("\n")))
        graph.edges[edge]["description"] = summarize_item(edge, descriptions, configured_llm)
        
    return graph