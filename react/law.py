from agents.law import law
from .prompt import law_react_prompt
from model.model_prep import Generator
from .loop import loop

law_known_actions = {
    "law": law
}

def law_ReAct(llm,state):
    global law_known_actions
    query=state["query"]
    iter_count=state["iter_count"]
    iter_count+=1
    prompt=law_react_prompt(query)
    generator = Generator(llm=llm,system=prompt)
    loop_res=loop(query=query,generator=generator,known_actions=law_known_actions)
    answer,react_process, action_agent, observations= (lambda x: x)(loop_res)
    return {"query":query,"agent":action_agent,"generate":answer,"react_res":react_process,"observations":observations,"iter_count":iter_count}