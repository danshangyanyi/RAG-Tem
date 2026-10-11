from langchain_core.documents import Document
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history

class Ragservice(object):

    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("systemm", "结合我提供的已知参考资料，"
                 "简洁和专业的回答用户问题，参考资料：{context}。"),
                 ("system", "并且我提供用户的对话历史记录，如下："),
                 MessagesPlaceholder("history"),
                 ("user","请回答问题：{input}")
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model_name)

        self.chain = self.__get_chian()


    def __get_chian(self):
        """获取最终执行链"""
        #获取检索器
        retriever = self.vector_service.get_retriever()

        def format_document(docs: list[Document]):
            if not docs:
                return "无资料"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"

        def fomat_for_retriever(value) -> str:
            return value["input"]

        def fomat_for_prompt_template(value):
            #{input, context, history}
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain = (
            {
                "input": RunnablePassthrough(),
                "content": RunnableLambda(fomat_for_retriever) | retriever | format_document
            } | RunnableLambda(fomat_for_prompt_template) | self.prompt_template | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain

