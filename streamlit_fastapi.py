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
    st.title(":blue[Search / Chat with finddme]")
    user_input = st.text_input('message')
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
                st.error(f"Error: {e}")
# ===============================================================================================================

if __name__ == '__main__':
    # asyncio.run(run_convo())
    run_convo()

# ===============================================================================================================

# if __name__ == '__main__':
#     asyncio.run(run_convo())
