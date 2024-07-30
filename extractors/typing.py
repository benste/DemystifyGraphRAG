from pydantic import BaseModel

class EntityExtractionResult(BaseModel):
    """Entity extraction result class definition."""

    entities: list[dict]
    graphml_graph: str | None
    
class SummarizationResult(BaseModel):
    """Unipartite graph extraction result class definition."""

    items: str | tuple[str, str]
    description: str