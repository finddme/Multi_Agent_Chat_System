"""
command:
streamlit run streamlit_fastapi.py

http://192.168.2.186:8501/
"""
import asyncio
from asyncio import run_coroutine_threadsafe
from threading import Thread
import os
import sys
import streamlit as st
import requests
import random
import time
from streamlit_chat import message
from langserve import RemoteRunnable
from pprint import pprint
import json
import io
from functools import reduce

async def get_response(user_input):
    print("user_input",user_input)
    client="http://192.168.2.186:7808/chat"
    headers = { 'Content-Type': 'application/json' }
    # response = requests.request("POST", client , headers=headers, data=json.dumps(user_input))
    user_input={"user_input": user_input}
    # response = requests.post(client, json.dumps(user_input))
    response = requests.request("POST", client , headers=headers, data=json.dumps(user_input))
    # print(response)
    return response

async def run_convo():
    st.title(""":blue[Multi-Agent search box]""")
    st.markdown("""
    <style>
    .small-font {
        font-size:12px !important;
        color:gray;
        margin-top: 0%;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(""":orange[**Law | Ai | conversation | web search | realtime | image**]""", 
                unsafe_allow_html=True 
                )
    # st.markdown("<p class='small-font'>정보를 요구하는 질문이 아닐 경우 일상 대화 chatbot 버전으로 사용할 수 있습니다.</p>",unsafe_allow_html=True)
    # st.markdown('---')
    # colored_header(label='', description='', color_name='gray-30')
    user_input = st.text_input('검색어를 입력하세요.')

    if user_input:
        with st.spinner("Processing..."):
            response = await get_response(user_input)
            try:
                try:
                    answer = response.json()['output']
                    agent = response.json()['agent'][0]
                    react_res=response.json()['react_res']

                    if len(react_res)!=0:
                        replacements={"\\n":"\n",
                            "\n":"",
                            "\n\n":"",
                            "Thought":"================>            **Thought**",
                            "Answer":"================>            **Answer**",
                            "Action":"================>            **Action**",
                            "Observation":"================>            **Observation**"}
                        replace_func = lambda text: reduce(lambda t, kv: t.replace(kv[0], kv[1]), replacements.items(), text)
                        react_res = replace_func(react_res)
                    else:pass
                    
                    result=f"""**Agent: [{agent.title()}]**\\
                            \\
                            {answer}\\
                            ----------------------------------------------------\\
                            **ReAct trajectory**\\
                            <p class='small-font'>{react_res}<\p>
                            """
                    st.markdown(result,unsafe_allow_html=True)

                except Exception as e:
                    img = response.content
                    st.image(io.BytesIO(img).getvalue(), caption="Sunrise by the mountains")
            except Exception as e:
                st.error(f"Error: {e}")

# ===============================================================================================================

if __name__ == '__main__':
    asyncio.run(run_convo())

