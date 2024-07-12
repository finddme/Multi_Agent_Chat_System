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

# #@st.cache_resource
async def get_response(user_input):
    # print("user_input",user_input)
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

async def run_convo():
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you?"}]
    
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
    
    st.title(":blue[Search / Chat with finddme]")
    # colored_header(label='', description='', color_name='gray-30')
    
    input_container = st.container() # 
    response_container = st.container() #
    
    # input_text = st.text_input('msg')
    # submitted = st.form_submit_button('Send')
    with st.form('form', clear_on_submit = True):
        user_input = st.text_input('msg')
        submitted = st.form_submit_button('Send')
    
    if 'user_responses' not in st.session_state:
        st.session_state['user_responses'] = []
    if 'bot_responses' not in st.session_state:
        st.session_state['bot_responses'] = []
    
    if submitted and user_input:
        with response_container: #
            if user_input:
                with st.spinner("Processing..."):
                    try:
                        answer, source = await get_response(user_input)
                        source= [s["source_title"].split("\n")[0] if s["source_title"] != " " else " " for s in source]
                        answer+= "\n\nsources->\n"+"\n".join(source)
                        # st.write(str(output)) ##
                        st.session_state.user_responses.append(user_input) #
                        st.session_state.bot_responses.append(str(answer)) #
                    except Exception as e:
                        st.error(f"Error: {e}")
    
            if st.session_state['bot_responses']:
                for i in range(len(st.session_state['bot_responses'])):
                    message(st.session_state['user_responses'][i], is_user=True, key=str(i) + '_user', 
                            # avatar_style="initials", seed="Kavita"
                            )
                    message(st.session_state['bot_responses'][i], key=str(i), 
                            # avatar_style="initials", seed="AI",
                            )
        with input_container:
            display_input = user_input

if __name__ == '__main__':
    asyncio.run(run_convo())

# ===============================================================================================================

# if __name__ == '__main__':
#     asyncio.run(run_convo())
