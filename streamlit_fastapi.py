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
from streamlit_extras.colored_header import colored_header
# """
# st.session_state 사용: 
# https://handmadesoftware.medium.com/streamlit-asyncio-and-mongodb-f85f77aea825
# """

# #@st.cache_resource
def get_response(user_input):
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

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you?"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# prompt = st.chat_input("Say something")
# if prompt:
#     st.write(f"User has sent the following prompt: {prompt}")
#     print(prompt)



# # https://medium.com/@kavita.kc/streamlit-and-chat-models-f4b80d1be391
# #Imports
# import streamlit as st
# from streamlit_chat import message
# from streamlit_extras.colored_header import colored_header

# #Streamlit UI Parameters
# st.title(":violet[Chat Bot via Streamlit]")
# colored_header(label='', description='', color_name='gray-30')


# # Initialize session state variables
# if 'user_responses' not in st.session_state:
#     st.session_state['user_responses'] = ["Hey"]
# if 'bot_responses' not in st.session_state:
#     st.session_state['bot_responses'] = ["Hey there! How may I help you today?"]

# input_container = st.container()
# response_container = st.container()

# # Capture user input and display bot responses
# user_input = st.text_input("You: ", "", key="input")

# print("//////////////////////////",user_input)
# with response_container:
#     if user_input:
#         response = get_response(user_input)
#         st.session_state.user_responses.append(user_input)
#         st.session_state.bot_responses.append(str(response))
        
#     if st.session_state['bot_responses']:
#         for i in range(len(st.session_state['bot_responses'])):
#             message(st.session_state['user_responses'][i], is_user=True, key=str(i) + '_user', avatar_style="initials", seed="Kavita")
#             message(st.session_state['bot_responses'][i], key=str(i), avatar_style="initials", seed="AI",)

# with input_container:
#     display_input = user_input

# ===============================================================================================================
# https://medium.com/gitconnected/langgraph-fastapi-and-streamlit-gradio-the-perfect-trio-for-ai-development-f1a82775496a
st.title(":blue[Search / Chat with finddme]")
colored_header(label='', description='', color_name='gray-30')

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
                    answer, source = get_response(user_input)
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


# ===============================================================================================================



# ===============================================================================================================
# async def run_convo():
#     st.header('Chatbot')

#     if 'generated_responses' not in st.session_state:
#         st.session_state['generated_responses'] = []

#     if 'user_inputs' not in st.session_state:
#         st.session_state['user_inputs'] = []

#     # if 'api_url' not in st.session_state:
#     #     st.session_state['api_url'] = ''

#     # if 'api_token' not in st.session_state:
#     #     st.session_state['api_token'] = ''

#     # st.session_state['api_url'] = st.text_input('API_URL: ', st.session_state['api_url'])
#     # st.session_state['api_token'] = st.text_input('API_TOKEN: ', st.session_state['api_token'],
#     #     type='password')

#     # def query(payload):
#     #     data = json.dumps(payload)
#     #     response = requests.request('POST',
#     #         st.session_state.api_url,
#     #         headers = {'Authorization': f'Bearer {st.session_state.api_token}'},
#     #         data = data)
#     #     return json.loads(response.content.decode('utf-8'))

#     with st.form('form', clear_on_submit = True):
#         user_input = st.text_input('Message: ')
#         submitted = st.form_submit_button('Send')

#     if submitted and user_input:
#         print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMM",user_input)
#         answer, source = get_response(user_input)
#         source= [aa["source_title"].split("\n")[0] if aa["source_title"] != " " else "web search result" for aa in a["source"]]
#         answer+= "\n"+"\n".join(source)
        
#         st.session_state.user_inputs.append(user_input)
#         st.session_state.generated_responses.append(answer)

#     if st.session_state['generated_responses']:
#         for i in range(0, len(st.session_state['generated_responses']), 1):
#             message(st.session_state['user_inputs'][i], is_user = True)
#             message(st.session_state['generated_responses'][i])
# ===============================================================================================================





# ===============================================================================================================
# async def run_convo():
#     # st.set_page_config("Chat PDF")

#     st.title("💬 Chatbot")
#     st.caption("🚀 A Streamlit chatbot powered by OpenAI")
#     if "messages" not in st.session_state:
#         st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

#     for msg in st.session_state.messages:
#         st.chat_message(msg["role"]).write(msg["content"])

#     if prompt := st.chat_input():
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         st.chat_message("user").write(prompt)
#         answer, source = get_response(prompt)
#         source= [aa["source_title"].split("\n")[0] if aa["source_title"] != " " else "web search result" for aa in a["source"]]
#         answer+= "\n"+"\n".join(source)
#         st.session_state.messages.append({"role": "assistant", "content": answer})
#         st.chat_message("assistant").write(answer)
# ===============================================================================================================


# ===============================================================================================================
# #@st.cache_resource
# async def run_convo():
#     # Initialize chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
        
#     # Display chat messages from history on app rerun
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Accept user input
#     if prompt := st.chat_input("Query"):
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         # Display user message in chat message container
#         with st.chat_message("user"):
#             st.markdown(prompt)
#         print(prompt)
#         # Display assistant response in chat message container
#         with st.chat_message("assistant"):
#             user_prompt = st.session_state.messages[-1]["content"]
#             print("!!!!!!!!!!!!!!!!!!!11111",user_prompt)
#             answer, source = await get_response(user_prompt)
#             source= [aa["source_title"].split("\n")[0] if aa["source_title"] != " " else "web search result" for aa in a["source"]]
#             answer+= "\n"+"\n".join(source)
#             response=st.write(answer) 
#         st.session_state.messages.append({"role": "assistant", "content": answer})
# ===============================================================================================================


# ===============================================================================================================
# #@st.cache_resource
# async def run_convo():
#     if "messages" not in st.session_state.keys():
#         st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]
        
#     # Display chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     # # User-provided prompt
#     # prompt = st.chat_input("Say something")
#     # if prompt := st.chat_input("Say something"):
#     if prompt := st.chat_input():
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)

#     # Generate a new response if last message is not from assistant
#     if st.session_state.messages[-1]["role"] != "assistant":
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 print("!!!!!!!!!!!!!!!!!!!!!11",prompt)
#                 print("!!!!!!!!!!!!!!!!!!!!!11",st.chat_input())
#                 response, source = await get_response(prompt)
#                 asyncio.create_task(coro)
#                 source= [aa["source_title"].split("\n")[0] if aa["source_title"] != " " else "web search result" for aa in a["source"]]
#                 response+= "\n"+"\n".join(source)
#                 st.write(response) 
#         message = {"role": "assistant", "content": response}
#         st.session_state.messages.append(message)
# ===============================================================================================================

# if __name__ == '__main__':
#     asyncio.run(run_convo())
