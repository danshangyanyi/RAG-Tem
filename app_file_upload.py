'''
基于Streamlit完成文件上传

Streamlit在WAB页面元素发生变化时，无论是上传还是刷新，代码都会重跑一遍，导致状态丢失
'''

import streamlit as st

from knowledge_base import KnowledgeBASEService

#网页标题
st.title("用户线上数据更新系统")

#文件上传接口
uploader_file = st.file_uploader(
    "txt文件上传入口",
    type=["txt"],
    accept_multiple_files=False,#单文件上传
)

#st.session_state#这是不会随着刷新重置的一个字典，用来保存信息

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBASEService()

if uploader_file is not None:
    #拿信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024

    st.subheader(f"文件名:{file_name}")
    st.write(f"格式：{file_type}|大小：{file_size:.2f}kb")

    #获取文件内容
    value = uploader_file.getvalue().decode("utf-8")
    
    result = st.session_state["service"].upload_by_str(value, file_name)
    st.write(result)



