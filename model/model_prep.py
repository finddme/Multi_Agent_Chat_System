import anthropic
from config import *
import os
import openai
from openai import OpenAI
import numpy as np
import random
import torch
import gc
import string
from diffusers import DiffusionPipeline
from huggingface_hub import login
import io
from io import BytesIO
from formats import *
import instructor
import json 
from tavily import TavilyClient
import cohere
import requests

Openai_API_KEY=API_KEY["Openai_API_KEY"]
coher_API_KEY=API_KEY["coher_API_KEY"]
TAVILY_API_KEY=API_KEY["TAVILY_API_KEY"]
claude_api_key=API_KEY["claude_api_key"]

hf_login= HF["login"]
# login(hf_login)

image_gen_endpoint= IMAGE["image_gen_endpoint"]

class Generator:
    def __init__(self, llm, system="",function=None):
        self.system = system
        self.llm = llm
        self.function = function
        self.messages = []
        self.model = "claude-3-5-sonnet-20240620"
        self.max_tokens=1024
    
    def __call__(self, message):
        # self.messages: list = [] # message 초기화 -> multiturn 필요 시, 관련 부분 수정
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self):
        if self.function:
            print("--- Function Calling ---")
            response=self.llm.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0,
                tools=self.function,
                messages=self.messages
            )
            return response
        else:
            print("--- ReAct ---")
            response = self.llm.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0,
                system = self.system,
                messages = self.messages
            )
            return response.content[0].text

def base_model():
    print("--- set base model ---")
    llm = anthropic.Anthropic(api_key=claude_api_key)
    return llm

def get_embedding_openai(text, engine="text-embedding-3-large") : 
    global Openai_API_KEY
    os.environ["OPENAI_API_KEY"] =  Openai_API_KEY
    openai.api_key =os.getenv("OPENAI_API_KEY")

    # res = openai.Embedding.create(input=text,engine=engine)['data'][0]['embedding']
    embedding_client = OpenAI()
    res= embedding_client.embeddings.create(input = text, model=engine).data[0].embedding
    return res

def keyword_conversion(text):
    global Output_format
    global Openai_API_KEY
    messages = [
        {
            "role": "system",
            "content": f"""Extract the key phrases from the following Korean sentence, translate each keyword into English, and list them.
                        The keywords should be separated by commas.

                        Example session:
                        Korean Sentence: 갈색 털의 짧은 다리 고양이가 해와 구름이 떠 있는 파란 하늘을 날고 있는 그림 그려줘
                        English Keywords: flying cat, brown fur, short legs, blue sky, clouds, sun
                        
                        Korean Sentence: {text}
                        English Keywords:
                        """
        }
    ]
    response = instructor.from_openai(OpenAI(api_key=Openai_API_KEY)).chat.completions.create(
        model='gpt-4o',
        response_model=Output_format,
        messages=messages
    )
    result = response.model_dump_json(indent=2)
    try:
        result=json.loads(result)
        result=list(map(lambda x: x["keyword"],result["keywords"]))
    except Exception as e: pass
    return result

def cohere_engine(coher_API_KEY=coher_API_KEY):
    co = cohere.Client(coher_API_KEY)
    return co

def tavily_engine(TAVILY_API_KEY=TAVILY_API_KEY):
    tavily = TavilyClient(api_key=TAVILY_API_KEY)
    return tavily

def img_model_call(query):
    data = json.dumps({"user_input": query}) 
    headers = { 'Content-Type': 'application/json'}
    response = requests.request("POST", image_gen_endpoint, headers=headers, data=data)
    img = response.content
    return io.BytesIO(img).getvalue()

def img_inference(pipe,device,MAX_SEED,prompt, 
                seed=42, randomize_seed=False, 
                width=1024, height=1024, 
                num_inference_steps=4):
    
    if randomize_seed:
        seed = random.randint(0, MAX_SEED)
    generator = torch.Generator().manual_seed(seed)
    image = pipe(
            prompt = prompt, 
            width = width,
            height = height,
            num_inference_steps = num_inference_steps, 
            generator = generator,
            guidance_scale=0.0
    ).images[0] 
    memory_stream = io.BytesIO()
    image.save(memory_stream, format="PNG")
    memory_stream.seek(0)
    return memory_stream