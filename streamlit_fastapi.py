import asyncio
from asyncio import run_coroutine_threadsafe
from threading import Thread
import os
import sys
import streamlit as st
import requests
import random
import time
# from streamlit_chat import message
# from langserve import RemoteRunnable
from pprint import pprint
import json
# from streamlit_extras.colored_header import colored_header
# """
# st.session_state 사용: 
# https://handmadesoftware.medium.com/streamlit-asyncio-and-mongodb-f85f77aea825
# """

async def get_response(user_input):
    print("user_input",user_input)
    client="http://192.168.2.186:8088/chat"
    headers = { 'Content-Type': 'application/json' }
    # response = requests.request("POST", client , headers=headers, data=json.dumps(user_input))
    user_input={"user_input": user_input}
    # response = requests.post(client, json.dumps(user_input))
    response = requests.request("POST", client , headers=headers, data=json.dumps(user_input))
    # print(response)
    answer = response.json()['output']
    source = response.json()['source']
    return answer,source

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you?"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# ===============================================================================================================
# https://medium.com/gitconnected/langgraph-fastapi-and-streamlit-gradio-the-perfect-trio-for-ai-development-f1a82775496a
async def run_convo():
    st.title(":blue[Search / Chat with finddme]")
    # colored_header(label='', description='', color_name='gray-30')
    user_input = st.text_input('msg')
    # submitted = st.form_submit_button('Send')

    if user_input:
        with st.spinner("Processing..."):
            try:
                # app = RemoteRunnable("http://192.168.2.186:8088/chat")
                # for output in app.stream({"input": input_text}):
                # input_text={"question": input_text}
                answer, source = await get_response(user_input)
                source= [s["source_title"].split("\n")[0] if s["source_title"] != " " else " " for s in source]
                if source[0] !=" ":
                    answer+= "\n\nsources->\n"+"\n".join(source)
                st.write(str(answer))
            
            except Exception as e:
                st.error(f"Error: {e}")
# ===============================================================================================================

# if __name__ == '__main__':
asyncio.run(run_convo())

# ===============================================================================================================

# if __name__ == '__main__':
#     asyncio.run(run_convo())
