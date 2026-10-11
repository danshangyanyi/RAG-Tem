import streamlit as st
from rag import Ragservice
import config_data as config

st.titke("简易rag")
st.divider()

#初始化，历史信息用session_state
if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"你好，有什么能够帮助您？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = Ragservice()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

#传递信息和模拟聊天窗口
if prompt:
    #输出提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user", "content":prompt})

    res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)

    ai_res_list = []

    def stream_ca(generator, cache_list):
        for chunk in generator:
            cache_list.append(chunk)
            yield chunk

    st.chat_message("assistant").write_stream(stream_ca(res_stream, ai_res_list))
    st.session_state["message"].append({"role":"assistant","content":"".join(ai_res_list)})#"".join(复数字符串)相当于把这些字符串连接起来


