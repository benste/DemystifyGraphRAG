from llama_cpp import Llama
from transformers import AutoTokenizer
import pandas as pd
import networkx as nx

from extractors.graph import graph_extractor, claim_extractor, descriptions_summarizer


# Load LLM
model_path = "models/gemma-2-9b-it-IQ4_XS.gguf"
tokenizer_URI = "google/gemma-2-9b-it"
context_size = 8192

configured_llm = {"llm": Llama(model_path=model_path, verbose=False, n_ctx=context_size)}
configured_llm["tokenizer"] = AutoTokenizer.from_pretrained(tokenizer_URI)

if configured_llm["tokenizer"].chat_template is None:
    chatnames = {"user": "user", "model": "assistant"}
elif "message['role'] == 'assistant'" in configured_llm["tokenizer"].chat_template:
    chatnames = {"user": "user", "model": "assistant"}
else:
    chatnames = {"user": "user", "model": "model"}
configured_llm["chatnames"] = chatnames    


# Data preprocessed by Microsoft GraphRAG
data_path = "datasets/ragtest/output/create_base_text_units.parquet"
preprocessed_data = pd.read_parquet(data_path)

# Entity Extraction
test_documents = dict(zip(preprocessed_data.chunk_id, preprocessed_data.chunk))
graph = graph_extractor.extract(test_documents, configured_llm)
nx.write_graphml(graph, "test_graph.graphml")

# Descriptions summarization
graph = nx.read_graphml("test_graph.graphml")
summarized_graph = descriptions_summarizer.summarize(graph, configured_llm)
nx.write_graphml(graph, "test_graph_descriptions_summarized.graphml")
1+1

