from agents.conversation import generate_conv
from agents.image import *
from react.info import info_ReAct
from react.law import law_ReAct
from HITL.hitl import res_check_hitl
from model.model_prep import *
from langgraph.graph import END, StateGraph
from formats import GraphState
from tools.function_call import *
from .node import Node
from db.db_management import ai_db_reload_auto

class Graph:
    def __init__(self,args):
        self.args=args
        global GraphState
        self.node=Node(self.args)
        if args.ai_db_restore=="yes":
            ai_db_reload_auto()

    async def graph_include_grader(self):
        global GraphState

        workflow = StateGraph(GraphState)

        # Define the nodes
        workflow.add_node("conversation", self.node.generate_conv_node) # retrieve
        workflow.add_node("info_ReAct", self.node.info_ReAct_node)
        # workflow.add_node("grade_documents", grade_documents) # grade documents
        workflow.add_node("image_generation", self.node.img_generation_node)
        workflow.add_node("law_ReAct", self.node.law_ReAct_node) # generatae
        # workflow.add_node("REDO", redo)

        workflow.add_edge("image_generation", END)
        workflow.add_edge("conversation", END)

        # Build graph
        workflow.set_conditional_entry_point(
            self.node.route_query_node,
            {
                "conversation": "conversation",
                "law": "law_ReAct",
                "information search":"info_ReAct",
                "image generation":"image_generation",
            },
        )
        
        workflow.add_conditional_edges(
            "info_ReAct", # start: node
            self.node.answer_grader_node, # defined function
            {
                "yes": END, #returns of the function
                "no": "info_ReAct",               #returns of the function
            },
        )

        workflow.add_conditional_edges(
            "law_ReAct", # start: node
            self.node.answer_grader_node, # defined function
            {
                "yes": END, #returns of the function
                "no": "law_ReAct",               #returns of the function
            },
        )

        # Compile
        app = workflow.compile()

        return app


    async def graph_simple_version(self):
        global GraphState

        workflow = StateGraph(GraphState)

        # Define the nodes
        workflow.add_node("conversation", self.node.generate_conv_node) # retrieve
        workflow.add_node("info_ReAct", self.node.info_ReAct_node)
        # workflow.add_node("grade_documents", grade_documents) # grade documents
        workflow.add_node("image_generation", self.node.img_generation_node)
        workflow.add_node("law_ReAct", self.node.law_ReAct_node) # generatae
        # workflow.add_node("REDO", redo)

        workflow.add_edge("image_generation", END)
        workflow.add_edge("conversation", END)
        workflow.add_edge("info_ReAct", END)
        workflow.add_edge("law_ReAct", END)

        # Build graph
        workflow.set_conditional_entry_point(
            self.node.route_query_node,
            {
                "conversation": "conversation",
                "law": "law_ReAct",
                "information search":"info_ReAct",
                "image generation":"image_generation",
            },
        )

        # Compile
        app = workflow.compile()

        return app
