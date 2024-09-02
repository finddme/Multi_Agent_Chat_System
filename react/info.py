import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.ai import ai
from agents.web_search import web_search
from agents.realtime import realtime
from .prompt import info_react_prompt
from model.model_prep import Generator
from .loop import loop

info_known_actions = {
    "web": web_search,
    "ai": ai,
    "realtime":realtime
}

def info_ReAct(llm,state):
    global info_known_actions
    query=state["query"]
    iter_count=state["iter_count"]
    iter_count+=1
    prompt=info_react_prompt(query)
    generator = Generator(llm=llm,system=prompt)
    loop_res=loop(query=query,generator=generator,known_actions=info_known_actions)
    answer,react_process, action_agent,observations= (lambda x: x)(loop_res)
    return {"query":query,"agent":action_agent,"generate":answer,"react_res":react_process,"observations":observations,"iter_count":iter_count}