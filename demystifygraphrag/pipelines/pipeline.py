from kedro.pipeline import Pipeline, node, pipeline

from demystifygraphrag.preprocessing import preprocess
from demystifygraphrag.load_llm import load_llm
from demystifygraphrag.entity_extraction import extract_entities
from demystifygraphrag.description_summarization import summarize_descriptions

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=load_llm.load_gemma2_gguf,
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
                func=extract_entities.raw_entities_to_graph,
                inputs=["raw_extracted_entities", "params:entity_extraction_prompt.formatting", "params:raw_entities_to_graph"],
                outputs="raw_entity_graph",
                name="parse_raw_entities_node",
            ),
            node(
                func=summarize_descriptions.summarize_descriptions,
                inputs=["raw_entity_graph", "llm", "params:summarize_descriptions_prompt", "params:summarize_descriptions"],
                outputs="entity_graph",
                name="summarize_descriptions_node",
            ),
        ]
    )
