import random
import torch
from model.model_prep import img_model_call,img_inference, keyword_conversion

def image_generation(state,args,pipe,device,MAX_SEED):
    query=state["query"]
    iter_count=state["iter_count"]
    iter_count+=1
    query_trasform=",".join(keyword_conversion(query))
    # print(query_trasform)
    if args.image=="endpoint":
        img_res=img_model_call(query_trasform)
    else:
        args.img_res=img_inference(pipe,device,MAX_SEED,query_trasform)
    return {"query":query,"agent":["image generation"],"generate":img_res,"react_res":"","observations":"","iter_count":iter_count}