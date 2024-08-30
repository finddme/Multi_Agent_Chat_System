from db.db_management import set_db_client
from config import DB
from model.model_prep import cohere_engine
from db.retrieve import *

client= set_db_client()

def law(query):
    global client

    law_weaviate_class=DB["law_weaviate_class"]

    retrieval_res=retrieve(query,law_weaviate_class)
    rerank_res=reranker_cohere(query,retrieval_res,law_weaviate_class)
    return rerank_res