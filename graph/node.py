from agents.conversation import generate_conv
from agents.image import *
from react.info import info_ReAct
from react.law import law_ReAct
from HITL.hitl import res_check_hitl
from model.model_prep import *
from tools.function_call import *

llm = base_model()

class Node:
    def __init__(self,args):
        self.args=args
        global llm

        if self.args.image=="model":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16

            self.pipe = DiffusionPipeline.from_pretrained(image_model, torch_dtype=dtype).to(device)
            self.MAX_SEED = np.iinfo(np.int32).max
            MAX_IMAGE_SIZE = 2048
        else: self.pipe,self.device,self.MAX_SEED=None,None,None

        if self.args.final_grader=="model": self.answer_grader=grade_answer
        elif self.args.final_grader=="hitl": self.answer_grader=res_check_hitl

    def generate_conv_node(self,state):
        global llm
        return generate_conv(state,llm)

    def img_generation_node(self,state):
        return image_generation(state,self.args,self.pipe,self.device,self.MAX_SEED)

    # @staticmethod
    def route_query_node(self,state):
        global llm
        return route_query(llm,state,self.args)

    def answer_grader_node(self,state):
        global llm
        return self.answer_grader(llm,state)

    def info_ReAct_node(self,state):
        global llm
        return info_ReAct(llm,state)

    def law_ReAct_node(self,state):
        global llm
        return law_ReAct(llm,state)

# def load_node(state,llm,pipe,device,MAX_SEED,answer_grader):
#     conversation_node=generate_conv_node(state,llm)
#     image=img_generation_node(state,pipe,device,MAX_SEED)
#     query_route=route_query_node(state,llm)
#     answer_grade=answer_grader_node(state,llm)
#     info=info_ReAct_node(state,llm)
#     law=law_ReAct_node(state,llm)
#     return locals()
