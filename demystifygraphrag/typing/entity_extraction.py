from typing import List

from pydantic import BaseModel, field_validator, Field

from demystifygraphrag.prompts.default_prompts import entity_extraction_prompts
  
  
class EntityExtractionPromptFormatting(BaseModel):
    tuple_delimiter: str = "<|>"  # delimiter between tuples in an output record, default is '<|>'
    record_delimiter: str = "##"  # delimiter between records, default is '##'
    completion_delimiter: str = "<|COMPLETE|>"
    entity_types: List[str] = ["organization", "person", "geo", "event"]
    input_text: str = None
    
class EntityExtractionPrompts(BaseModel):
    entity_extraction_prompt: str = entity_extraction_prompts.ENTITY_EXTRACTION_PROMPT
    continue_prompt: str = entity_extraction_prompts.CONTINUE_PROMPT
    loop_prompt: str = entity_extraction_prompts.LOOP_PROMPT
    
class EntityExtractionPromptParams(BaseModel):
    prompts: EntityExtractionPrompts
    formatting: EntityExtractionPromptFormatting
    
class EntityExtractionParams(BaseModel):
    max_gleans: int = 5
    column_to_extract: str = 'chunk'
    results_column: str = 'raw_entities'
    
class ParseRawEntitiesParams(BaseModel):
    raw_entities_column: str = 'raw_entities'
    reference_column: str = 'chunk_id'  # source_id will be added to the edged and nodes. This allows source reference when quiring the graph

class EntityExtractionResult(BaseModel):
    """Entity extraction result class definition."""

    entities: list[dict]
    graphml_graph: str | None
    