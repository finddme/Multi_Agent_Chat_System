"""
command:
streamlit run streamlit_fastapi.py

http://192.168.2.186:8501/
"""
import asyncio
import streamlit as st
import requests
import json
import io
from functools import reduce

async def get_response(user_input):
    client="http://eleven.acryl.ai:37808/chat"
    headers = { 'Content-Type': 'application/json' }
    user_input={"user_input": user_input}
    response = requests.request("POST", client , headers=headers, data=json.dumps(user_input))
    return response

async def run_convo():
    # st.title(""":blue[Multi-Agent search box]""")
    st.markdown("""
    <style>
    .small-font {
        font-size:12px !important;
        color:gray;
        margin-top: 0%;
    }
    </style>
    """, unsafe_allow_html=True)
    # st.markdown("""**검색어를 입력하세요.**\\
    #             :orange[**Law | Ai | conversation | web search | realtime | image generation**]""", 
    #             unsafe_allow_html=True 
    #             )
    user_input = st.text_input('')

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
    # st.image("https://finddme.github.io/public/react2.png", caption="search box pipeline")
    
if __name__ == '__main__':
    asyncio.run(run_convo())

