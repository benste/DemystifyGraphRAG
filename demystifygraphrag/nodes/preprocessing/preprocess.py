import os
from typing import List
from collections import defaultdict

import pandas as pd

from demystifygraphrag.llm.base_llm import LLM
from demystifygraphrag.nodes.preprocessing import utils


def raw_documents(config: dict) -> pd.DataFrame:
    """
      loads files from folder path and subfolders.
    """
    
    # Walk the folder path, find text files and load them
    folder_path = config['raw_documents_folder']
    df = defaultdict(list)
    file_id = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                df["document_path"].append(os.path.join(root, file))
                df["content"].append(open(df["document_path"][-1], "r").read())
                df["document_id"].append(str(file_id))
                file_id += 1
        
    return pd.DataFrame(df)


def orderby(dataframe: pd.DataFrame, config: dict) -> pd.DataFrame:
    """order pandas dataframe my keys in order

    Args:
        dataframe (pd.DataFrame): to sort
        config (OrderByConfig): keys = what to order on, acending = 'asc' | 'desc

    Returns:
        pd.DataFrame
    """
    
    config = config['orderby']
    ascending = [asc == "asc" for asc in config['ascending']]
    return dataframe.sort_values(by=config['keys'], ascending=ascending)
  

def zip_colums(dataframe: pd.DataFrame, config: dict) -> pd.DataFrame:
    config = config['zip_columns']
    
    dataframe[config['to']] = list(zip(*[dataframe[col] for col in config['columns']], strict=True))
    return dataframe.reset_index(drop=True)


def chunk(dataframe: pd.DataFrame, llm: LLM, config: dict) -> pd.DataFrame:
    column_to_chunk = config['chunk'].get("column_to_chunk") or "content"
    window_size = config['chunk'].get("window_size")
    overlap = config['chunk'].get("overlap")
    
    # Apply chunking per document, also saving the number of tokens in each chunk
    dataframe['chunk'], dataframe['chunk_len'] = zip(*dataframe[column_to_chunk].apply(lambda c: utils.chunk_text(c, llm, window_size, overlap)))
    
    # Put each chunk in it's own row, keeping the original document content and id 
    dataframe = dataframe.explode(["chunk", "chunk_len"])
    
    # Give each chunk a unique ID
    dataframe['chunk_id'] = list(range(len(dataframe)))
    
    # TODO: drop content column to save space?
    
    return dataframe
    