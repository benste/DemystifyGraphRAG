from dagster import asset
import pandas as pd

from demystifygraphrag.ops import preprocess_documents as preprocess_ops
from demystifygraphrag.llm import llm, gemma2

@asset
def preprocess() -> pd.DataFrame:
    # Load LLM and tokenizer
    loaded_llm = llm.llm(gemma2.gemma2_instance)
    
    # Load raw text
    config = preprocess_ops.RawDocumentsConfig(folder_path="/home/bens/projects/DemystifyGraphRAG/datasets/ragtest/dickens")
    docs = preprocess_ops.raw_documents(raw_documents_config=config)
    
    # Order documents by ID
    config = preprocess_ops.OrderByConfig(keys=['document_id'], ascending=['desc'])
    docs = preprocess_ops.orderby(docs, orderby_config=config)
    
    # Pack the document ids with the text
    # So when we unpack the chunks, we can restore the document id
    config = preprocess_ops.ZipConfig(columns=["document_id", "content"], to="content_with_ids")
    docs = preprocess_ops.zip_colums(docs, zip_config=config)
    
    return docs