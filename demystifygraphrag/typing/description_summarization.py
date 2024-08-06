from typing import List

from pydantic import BaseModel, field_validator, Field

from demystifygraphrag.prompts.default_prompts import summarization_prompts
  
  
class DescriptionSummarizationPromptFormatting(BaseModel):
    entity_names: List[str]
    description_list: List[str]
    
class DescriptionSummarizationPromptParams(BaseModel):
    prompt: str = summarization_prompts.SUMMARIZE_PROMPT
    formatting: DescriptionSummarizationPromptFormatting


# class EntityExtractionResult(BaseModel):
#     """Entity extraction result class definition."""

#     entities: list[dict]
#     graphml_graph: str | None
    