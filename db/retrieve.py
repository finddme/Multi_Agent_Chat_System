import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .db_management import set_db_client
from model.model_prep import cohere_engine, get_embedding_openai
import cohere
import re
from config import *

client= set_db_client()
co= cohere_engine()

def retrieve(query,weaviate_class):
    global client
    print("--- Retrieve vectorstore ---")
    query_vector = get_embedding_openai(query)
    property_list = list(map(lambda x: x["name"], client.schema.get(weaviate_class)['properties']))
    response = client.query.get(weaviate_class,property_list).with_hybrid(query, vector=query_vector).with_limit(3).do()
    return response

def reranker_cohere(query,documents_co,weaviate_class):
    global client
    global co
    print("--- RERANK ---")
    # weaviate_class=weaviate_class.title()
    weaviate_class=weaviate_class.capitalize()

    if weaviate_class=="Law":
        documents=[r["full_content"] for r in documents_co["data"]["Get"][weaviate_class]]
        documents=list(dict.fromkeys(documents))
    else:
        documents=[r["text"] for r in documents_co["data"]["Get"][weaviate_class]]
        source=[{"source_title":r["source_title"],"source":r["source"]} for r in documents_co["data"]["Get"][weaviate_class]]
    
    rerank_res = co.rerank(
        model="rerank-multilingual-v3.0",
        query=query,
        documents=documents, 
        top_n=4, 
    )
    
    doc_txt = ""
    
    for idx,result in enumerate(rerank_res.results):
        doc_txt += f"doc {idx}. {documents[result.index]} \n"

    final_res=filter_sentences(doc_txt)
    
    return final_res

def filter_sentences(text):
    pattern = r'^(?:[A-Za-z\u3131-\u318E\uAC00-\uD7A3\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u00FF\u0020-\u007E]+$|$)'
    return '\n'.join(line for line in text.split('\n') if re.match(pattern, line))