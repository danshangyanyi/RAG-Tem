md5_path = './md5.txt'
collection_name = 'rag'
persist_directorty = './chroma.db'
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "。", "！", "?", "？", ",", "，"]
max_split_char_number = 1000 #文本分割阈值，不超过不分割

similiarity_threshold = 2 #检索返回几份文档/信息

embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3.7-plus"

session_config = {"configurable":{"session_id":"user_001"}}