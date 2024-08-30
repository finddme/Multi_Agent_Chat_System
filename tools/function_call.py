import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .tool import *
from model.model_prep import Generator

def route_query(llm,state,args):
    global routing_function

    if args.image=="none":routing_function=routing_simple
    else:routing_function=routing_include_imggen

    query = state["query"]
    query_router = Generator(llm=llm,function=routing_function)
    response=query_router(query)
    for content in response.content:
        if content.type == "tool_use" and content.name == "query_routing":
            q_type = content.input
            break
    return q_type["query"]

def grade_answer(llm,state):
    global grading_answer
    observations = state["observations"]
    generate = state["generate"]
    iter_count=state["iter_count"]
    print(f"--- answer grading {iter_count}---")
    if iter_count >2:
        return "yes"
    else:
        answer_check=f"Set of facts: \n\n {observations} \n\n LLM generation: {generate}"
        answer_grader = Generator(llm=llm,function=grading_answer)
        response=answer_grader(answer_check)
        for content in response.content:
            if content.type == "tool_use" and content.name == "hallucination_grader":
                grade_res = content.input
                break
        grade_res=grade_res["answer_grading"]
        return grade_res