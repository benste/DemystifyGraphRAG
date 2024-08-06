from kedro.pipeline import Pipeline, node, pipeline

from demystifygraphrag.nodes.preprocessing import preprocess
from demystifygraphrag.nodes.llm import initialize_llm
from demystifygraphrag.nodes.entity_extraction import extract_entities

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=initialize_llm.initialize_gemma2_gguf,
                inputs=["params:llm"],
                outputs="llm",
                name="llm_loader_node",
            ),
            node(
                func=preprocess.raw_documents,
                inputs=["params:preprocess.raw_documents"],
                outputs="raw_docs",
                name="raw_documents_node",
            ),
            node(
                func=preprocess.chunk,
                inputs=["raw_docs", "llm", "params:preprocess.chunk"],
                outputs="chunked_docs",
                name="chunk_node",
            ),
            node(
                func=extract_entities.raw_entity_extraction,
                inputs=["chunked_docs", "llm", "params:entity_extraction_prompt", "params:entity_extraction"],
                outputs="raw_extracted_entities",
                name="raw_entity_extraction_node",
            ),
            node(
                func=extract_entities.parse_raw_entities,
                inputs=["raw_extracted_entities", "params:entity_extraction_prompt.formatting", "params:parse_raw_entities"],
                outputs="entity_graph",
                name="parse_raw_entities_node",
            ),
            
        ]
    )
