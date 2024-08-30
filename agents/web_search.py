from tavily import TavilyClient
from langchain.schema import Document
from model.model_prep import tavily_engine
import httpx

tavily = tavily_engine()

def wikipedia(query):
    try:
        return httpx.get("https://ko.wikipedia.org/w/api.php", params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }).json()["query"]["search"][0]["snippet"]
    except Exception as e: return None

def web_search_tavily(query):
    global tavily
    tavily_response = tavily.search(query=query,search_depth="advanced")
    tavily_response2 = tavily.qna_search(query=query, search_depth="advanced",max_results =3)
    web_results = "\n".join([d["content"] for d in tavily_response["results"]])
    web_results+=f"\n{tavily_response2}"
    # web_results = Document(page_content=web_results)

    return web_results

def web_search(query):
    wiki_res=wikipedia(query)
    tavily_res=web_search_tavily(query)
    web_search_res=f"{tavily_res} \n {wiki_res}"
    return web_search_res