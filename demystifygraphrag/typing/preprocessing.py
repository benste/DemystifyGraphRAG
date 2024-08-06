from pydantic import BaseModel
import pandas as pd
    
class RawDocumentsParams(BaseModel):
    """Params for raw document loading"""
    raw_documents_folder: str  # Folder to search for text documents
    raw_content_column: str = 'content'  # Name of the dataframe column to store each document's content
    
class ChunkParams(BaseModel):
    """Params for chunking documents"""
    column_to_chunk: str = 'content'  # Column to chunk
    results_column: str = 'chunk'  # Column to write chunks to
    id_column: str = 'chunk_id'  # column with which to later refence the source text
    window_size: int = 300  # Number of tokens in each chunk
    overlap: int = 100  # Number of tokens chunks overlap
    
class PreprocessParams(BaseModel):
    """Params for preprocessing raw documents"""
    raw_documents: RawDocumentsParams
    chunk: ChunkParams
    
