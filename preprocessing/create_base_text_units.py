# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""A module containing build_steps method definition."""

from datashaper import DEFAULT_INPUT_NAME

from graphrag.index.config import PipelineWorkflowStep

workflow_name = "create_base_text_units"


def build_steps(
) -> list[PipelineWorkflowStep]:
    """
    Create the base table for text units.

    ## Dependencies
    None
    """
    chunk_column_name = 'chunk' # config.get("chunk_column", "chunk")
    chunk_by_columns = ['id'] # config.get("chunk_by", []) or []
    n_tokens_column_name = 'n_tokens' # config.get("n_tokens_column", "n_tokens")
    chunks = {'strategy': {'type': "tokens", 'chunk_size': 300, 'chunk_overlap': 100, 'group_by_columns': ['id']}}
    return [
        {
            "verb": "orderby",
            "args": {
                "orders": [
                    # sort for reproducibility
                    {"column": "id", "direction": "asc"},
                ]
            },
            "input": {"source": DEFAULT_INPUT_NAME},
        },
        {
            "verb": "zip",
            "args": {
                # Pack the document ids with the text
                # So when we unpack the chunks, we can restore the document id
                "columns": ["id", "text"],
                "to": "text_with_ids",
            },
        },
        {
            "verb": "aggregate_override",
            "args": {
                "groupby": [*chunk_by_columns] if len(chunk_by_columns) > 0 else None,
                "aggregations": [
                    {
                        "column": "text_with_ids",
                        "operation": "array_agg",
                        "to": "texts",
                    }
                ],
            },
        },
        {
            "verb": "chunk",
            # "args": {"column": "texts", "to": "chunks", **config.get("text_chunk", {})},
            "args": {"column": "texts", "to": "chunks", **chunks},
        },
        {
            "verb": "select",
            "args": {
                "columns": [*chunk_by_columns, "chunks"],
            },
        },
        {
            "verb": "unroll",
            "args": {
                "column": "chunks",
            },
        },
        {
            "verb": "rename",
            "args": {
                "columns": {
                    "chunks": chunk_column_name,
                }
            },
        },
        {
            "verb": "genid",
            "args": {
                # Generate a unique id for each chunk
                "to": "chunk_id",
                "method": "md5_hash",
                "hash": [chunk_column_name],
            },
        },
        {
            "verb": "unzip",
            "args": {
                "column": chunk_column_name,
                "to": ["document_ids", chunk_column_name, n_tokens_column_name],
            },
        },
        {"verb": "copy", "args": {"column": "chunk_id", "to": "id"}},
        {
            # ELIMINATE EMPTY CHUNKS
            "verb": "filter",
            "args": {
                "column": chunk_column_name,
                "criteria": [
                    {
                        "type": "value",
                        "operator": "is not empty",
                    }
                ],
            },
        },
    ]
