routing_include_imggen=[
        {
            "name": "query_routing",
            "description": """
        You are an expert at routing a user question to a law or casual conversation or image generation or information search.
        If the question is a casual conversation use original knowledge.
        If it does not fall under law or casual conversation or image generation, it is classified as information search.
            Given a user question choose to route it to law or casual conversation or image generation or information search""",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "enum": ["conversation", "law", "information search", "image generation"],
                        "description": "route query to casual conversation or web search or a vectorstore or law or image generation or realtime news."
                    }
                },
                "required": ["query"]
            }
        }
    ]
routing_simple=[
        {
            "name": "query_routing",
            "description": """
        You are an expert at routing a user question to a law or casual conversation or information search.
        If the question is a casual conversation use original knowledge.
        If it does not fall under law or casual conversation, it is classified as information search.
            Given a user question choose to route it to law or casual conversation or information search""",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "enum": ["conversation", "law", "information search"],
                        "description": "route query to casual conversation or web search or a vectorstore or law or image generation or realtime news."
                    }
                },
                "required": ["query"]
            }
        }
    ]

grading_answer=[
        {
            "name": "hallucination_grader",
            "description": """
                You are a grader assessing whether an LLM generation is supported by a set of retrieved facts. \n 
                Restrict yourself to give a binary score, either 'yes' or 'no'. If the answer is supported or partially supported by the set of facts, consider it a yes. \n
                Don't consider calling external APIs for additional information as consistent with the facts.""",
            "input_schema": {
                "type": "object",
                "properties": {
                    "answer_grading": {
                        "type": "string",
                        "enum": ["yes", "no"],
                        "description": "Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."
                    }
                },
                "required": ["answer_grading"]
            }
        }
    ]
