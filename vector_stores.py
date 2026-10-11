from langchain_chroma import Chroma
import config_data as config

class VectorStoreService(object):
    def __init__(self, embedding):
        """
        embedding: 嵌入模型
        """
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directorty,
        )

    def get_retriever(self):
        """
        返回向量检索器,Chroma里自带了向量检索
        但不应该是vector_store.similarity_search吗
        """
        return self.vector_store.as_retriever(search_kwargs={"k": config.similiarity_threshold})

    