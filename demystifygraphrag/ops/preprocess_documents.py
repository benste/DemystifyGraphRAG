import os
from typing import List
from collections import defaultdict

from dagster import op, Config
import pandas as pd

class RawDocumentsConfig(Config):
    folder_path: str


@op
def raw_documents(raw_documents_config: RawDocumentsConfig) -> pd.DataFrame:
    """
      loads files from folder path.
    """
    folder_path = raw_documents_config.folder_path
    
    df = defaultdict(list)
    file_id = 0
    for file in os.listdir(folder_path):
      if file.endswith('.txt'):
        df["document_path"].append(os.path.join(folder_path, file))
        df["content"].append(open(df["document_path"][-1], "r").read())
        df["document_id"].append(str(file_id))
        
    return pd.DataFrame(df)
        
        
class OrderByConfig(Config):
    keys: list = ['document_id']
    ascending: list = ['asc']


def orderby_noop(dataframe: pd.DataFrame, config: OrderByConfig) -> pd.DataFrame:
    """order pandas dataframe my keys in order

    Args:
        dataframe (pd.DataFrame): to sort
        config (OrderByConfig): keys = what to order on, acending = 'asc' | 'desc

    Returns:
        pd.DataFrame
    """
    print(f"oder by config: {config}")
    ascending = [asc == "asc" for asc in config.ascending]
    return dataframe.sort_values(by=config.keys, ascending=ascending)

@op
def orderby(dataframe: pd.DataFrame, orderby_config: OrderByConfig) -> pd.DataFrame:
    """order pandas dataframe my keys in order

    Args:
        dataframe (pd.DataFrame): to sort
        config (OrderByConfig): keys = what to order on, acending = 'asc' | 'desc

    Returns:
        pd.DataFrame
    """
    ascending = [asc == "asc" for asc in orderby_config.ascending]
    return dataframe.sort_values(by=orderby_config.keys, ascending=ascending)
  
class ZipConfig(Config):
    columns: List[str] = ['document_id', 'content']
    to: str = 'content_with_ids'
                  
@op
def zip_colums(dataframe: pd.DataFrame, zip_config: ZipConfig) -> pd.DataFrame:
    dataframe[zip_config.to] = list(zip(*[dataframe[col] for col in zip_config.columns], strict=True))
    return dataframe.reset_index(drop=True)

class ChunkConfig(Config):
    chunk_size: int = 300
    chunk_overlap: int = 100
    chunk_column: str = 'content'
    group_by_columns: List[str] = ['document_id']
    
# @op
# def chunk(dataframe: pd.DataFrame, config: ChunkConfig) -> pd.DataFrame:
    