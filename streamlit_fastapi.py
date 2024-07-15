import asyncio
from asyncio import run_coroutine_threadsafe
from threading import Thread
import os
import sys
import streamlit as st
import requests
import random
import time
from pprint import pprint
import json


# async def get_response(user_input):
def get_response(user_input):
    # client="http://192.168.2.186:8088/chat"
    client="http://eleven.acryl.ai:37808/chat"
    headers = { 'Content-Type': 'application/json' }
    user_input={"user_input": user_input}
    response = requests.request("POST", client , headers=headers, data=json.dumps(user_input))
    answer = response.json()['output']
    source = response.json()['source']
    return answer,source

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you?"}]

# Inject custom CSS to set the width of the sidebar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 50px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# st.sidebar.button('Clear History', on_click=clear_chat_history)
# async def run_convo():
def run_convo():
    # st.title(""":blue[Search / Chat with finddme]""")
    # st.title(""":blue[RAG 기반 블로그 검색창]""")
    st.markdown("""
    <style>
    .custom-font {
        font-weight: bold;
        font-size:28px !important;
        color: #0067C8;
        margin-top: 0%;
        font-family: Arial, Helvetica, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .custom-font2 {
        font-size:12px !important;
        color: gray;
        margin-top: 0%;
        font-family: Arial, Helvetica, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""<p class='custom-font'>😎 RAG 기반 블로그 검색창</p>""", unsafe_allow_html=True )

    st.markdown("""3 pipeline (1)LLM/NLP/AI->블로그 포스트 RAG (2)일반 질문->Web search RAG (3)일상 대화->일반 chatbot</p>""", 
                unsafe_allow_html=True 
                )
    # st.markdown(""":orange[*Query Router | Hallucination Grader | Reranker | Web search*<br><p class='small-font'>인공지능/LLM/NLP와 관련된 질문은 본 <strong>블로그 포스트</strong>를 기반으로 답변하고, 
    #             일반적인 질문은 <strong>web search</strong>를 통해 답변합니다.
    #             정보를 요구하는 질문이 아닐 경우 <strong>일상 대화 chatbot 버전</strong>으로 사용할 수 있습니다.</p>]""", 
    #             unsafe_allow_html=True 
    #             )
    user_input = st.text_input('검색어를 입력하세요. :orange[*Query Router | Hallucination Grader | Reranker | Web search*]')
    # submitted = st.form_submit_button('Send')
    
    if user_input:
        with st.spinner("Processing..."):
            try:
                # answer, source = await get_response(user_input)
                answer, source = get_response(user_input)
                source= [s["source_title"].split("\n")[0] if s["source_title"] != " " else " " for s in source]
                if source[0] !=" ":
                    answer+= "\n\nsources->\n"+"\n".join(source)
                st.write(str(answer))
            
            except Exception as e:
                error_msg="Need to check port-forwarding status: Need to verify the server running FastAPI (port 7808)"
                st.error(f"Error: {error_msg}")
                # st.error(f"Error: {e}")
# ===============================================================================================================

if __name__ == '__main__':
    # asyncio.run(run_convo())
    run_convo()

# ===============================================================================================================

# if __name__ == '__main__':
#     asyncio.run(run_convo())
