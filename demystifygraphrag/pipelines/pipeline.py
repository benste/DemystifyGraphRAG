from kedro.pipeline import Pipeline, node, pipeline

from demystifygraphrag.nodes.preprocessing import preprocess
from demystifygraphrag.nodes.llm import initialize_llm

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
                inputs=["params:preprocess"],
                outputs="raw_docs",
                name="raw_documents_node",
            ),
            node(
                func=preprocess.chunk,
                inputs=["raw_docs", "llm", "params:preprocess"],
                outputs="chunked_docs",
                name="chunk_node",
            ),
        ]
    )
