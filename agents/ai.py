from db.db_management import set_db_client
from config import DB
from model.model_prep import cohere_engine
from db.retrieve import *

client= set_db_client()

def ai(query):
    global client
    ai_weaviate_class=DB["ai_weaviate_class"]

    retrieval_res=retrieve(query,ai_weaviate_class)
    rerank_res=reranker_cohere(query,retrieval_res,ai_weaviate_class)
    return rerank_res