from collections.abc import Mapping
import re
import numbers

import networkx as nx

from demystifygraphrag.llm.base_llm import LLM
from demystifygraphrag.nodes.preprocessing.utils import clean_str
    
def loop_extraction(documents: dict[int: str], formatting: dict, llm: LLM, max_gleans: int = 5):
    completion_delimiter = formatting['completion_delimiter']
    
    llm_raw_output = {}
    for source_chunk_id, doc in documents.items():
        print(f"\n-->processing chunk {len(llm_raw_output)+1} of {len(documents)}")
        formatting['input_text'] = doc
    
        # First entity extraction
        prompt = formatting['default_prompt'].format(**formatting)
        chat = llm.format_chat([("user", prompt)])
        raw_output = llm.run_chat(chat).removesuffix(completion_delimiter)
        llm_raw_output[source_chunk_id] = raw_output
        chat = llm.format_chat([("model", raw_output)], chat)
        
        # Extract more entities LLM might have missed first time around
        for g in range(max_gleans):
            # Get more entities
            print(f"\n-->trying to get more entities out of chunk ({g+1} / max {max_gleans})")
            chat = llm.format_chat([("user", formatting['continue_prompt'])], chat)
            raw_output = llm.run_chat(chat).removesuffix(completion_delimiter)
            llm_raw_output[source_chunk_id] += formatting['record_delimiter'] + raw_output or ""
            chat = llm.format_chat([("model", raw_output)], chat)

            # Check if the LLM thinks there are still entities missing
            loop_chat = llm.format_chat([("user", formatting['loop_prompt'])], chat)
            continuation = llm.run_chat(loop_chat).removesuffix(completion_delimiter)
            if continuation.lower() != "yes":
                break
                
    return llm_raw_output

def _unpack_source_ids(data: Mapping) -> list[str]:
    value = data.get("source_id", None)
    return [] if value is None else value.split(", ")

def process_graph_results(
        results: dict[int, str],
        tuple_delimiter: str,
        record_delimiter: str,
    ) -> nx.Graph:
        """Parse the result string to create an undirected unipartite graph.

        Args:
            - results - dict of results from the extraction chain
            - tuple_delimiter - delimiter between tuples in an output record, default is '<|>'
            - record_delimiter - delimiter between records, default is '##'
        Returns:
            - output - unipartite graph in graphML format
        """
        graph = nx.Graph()
        for source_doc_id, extracted_data in results.items():
            records = [r.strip() for r in extracted_data.split(record_delimiter)]

            for record in records:
                record = re.sub(r"^\(|\)$", "", record.strip())
                record_attributes = record.split(tuple_delimiter)

                if record_attributes[0] == '"entity"' and len(record_attributes) >= 4:
                    # add this record as a node in the G
                    entity_name = clean_str(record_attributes[1].upper())
                    entity_type = clean_str(record_attributes[2].upper())
                    entity_description = clean_str(record_attributes[3])

                    if entity_name in graph.nodes():
                        node = graph.nodes[entity_name]
                        if len(entity_description) > len(node["description"]):
                            node["description"] = entity_description
                        node["source_id"] = ", ".join(
                            list({
                                *_unpack_source_ids(node),
                                str(source_doc_id),
                            })
                        )
                        node["entity_type"] = (
                            entity_type if entity_type != "" else node["entity_type"]
                        )
                    else:
                        graph.add_node(
                            entity_name,
                            type=entity_type,
                            description=entity_description,
                            source_id=str(source_doc_id),
                        )

                if (
                    record_attributes[0] == '"relationship"'
                    and len(record_attributes) >= 5
                ):
                    # add this record as edge
                    source = clean_str(record_attributes[1].upper())
                    target = clean_str(record_attributes[2].upper())
                    edge_description = clean_str(record_attributes[3])
                    edge_source_id = clean_str(str(source_doc_id))
                    weight = (
                        float(record_attributes[-1])
                        if isinstance(record_attributes[-1], numbers.Number)
                        else 1.0
                    )
                    if source not in graph.nodes():
                        graph.add_node(
                            source,
                            type="",
                            description="",
                            source_id=edge_source_id,
                        )
                    if target not in graph.nodes():
                        graph.add_node(
                            target,
                            type="",
                            description="",
                            source_id=edge_source_id,
                        )
                    if graph.has_edge(source, target):
                        edge_data = graph.get_edge_data(source, target)
                        if edge_data is not None:
                            weight += edge_data["weight"]
                            edge_source_id = ", ".join(
                                list({
                                    *_unpack_source_ids(edge_data),
                                    str(source_doc_id),
                                })
                            )
                    graph.add_edge(
                        source,
                        target,
                        weight=weight,
                        description=edge_description,
                        source_id=edge_source_id,
                    )

        return graph
