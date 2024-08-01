# from typing import List

# from dagster import job, op, RunConfig

# from demystifygraphrag.assets.preprocess_documents import raw_documents, raw_documents_config
# from demystifygraphrag.ops.preprocess_documents import orderby, OrderByConfig, zip, ZipConfig

# @job()
# def preprocess():
#     # Load raw text
#     raw_docs = raw_documents()
    
#     # Order documents by ID
#     @op
#     def oderby_config():
#         return OrderByConfig(keys=['id'], ascending=['desc'])
#     raw_docs = orderby(dataframe=raw_docs, orderby_config=oderby_config())
    
#     # Pack the document ids with the text
#     # So when we unpack the chunks, we can restore the document id
#     @op
#     def zip_config():
#         return ZipConfig(columns=["id", "text"], to="text_with_ids")
#     raw_docs = zip(raw_documents, zip_config=zip_config())