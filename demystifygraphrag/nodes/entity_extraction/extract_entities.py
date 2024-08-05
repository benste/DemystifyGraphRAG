import pandas as pd

from demystifygraphrag.prompts.default_prompts import entity_extraction_prompts
from demystifygraphrag.nodes.entity_extraction.typing import EntityExtractionResult
from demystifygraphrag.nodes.entity_extraction.utils import loop_extraction, process_graph_results
from demystifygraphrag.llm.base_llm import LLM


def extract(dataframe: pd.DataFrame, llm: LLM, config: dict) -> tuple:
    max_gleans = config.get("max_gleans")
    documents_column = config.get("documents_columns")
    
    # Prompt formatting
    formatting = entity_extraction_prompts.DEFAULT_FORMATTING
    formatting['default_prompt'] = entity_extraction_prompts.GRAPH_EXTRACTION_PROMPT
    formatting['continue_prompt'] = entity_extraction_prompts.CONTINUE_PROMPT
    formatting['loop_prompt'] = entity_extraction_prompts.LOOP_PROMPT
    
    llm_raw_output = loop_extraction(dataframe[documents_column], formatting, llm, max_gleans)
        
    graph = process_graph_results(llm_raw_output, formatting['tuple_delimiter'], formatting['record_delimiter'])
    
    # Get a list of entities from the graph
    entities = [
        ({"name": item[0], **(item[1] or {})})
        for item in graph.nodes(data=True)
        if item is not None
    ]

    return EntityExtractionResult(entities=entities, graphml_graph=graph)

