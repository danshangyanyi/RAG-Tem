'''
知识库相关操作
'''
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


os.environ["DASHSCOPE_API_KEY"] = "sk-ws-H.EDLLPXI.hq1v.MEYCIQCwfCKQ8l8XdMFfohVIg0IveFN_ngH3r4TXQeOR8QFheAIhANozNH2MSaOuuBAAHw1ct_Vqs2O7QPYo-UjCFINIXhoF"

def check_md5(md5_str: str):
    '''
    检查传入字符串是否重复（True,False）
    '''
    if not os.path.exists(config.md5_path):
        '''若文件不存在'''
        open(config.md5_path, 'w', encoding="utf-8").close()
        return False
    else:
        '''文件存在'''
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()#处理掉空格和回车
            if line == md5_str:
                return True#好弱智的处理法，完全可以数据库内文本排序然后首字符检索

    return False

def save_md5(md5_str: str):
    '''将传入的信息记录并保存'''
    with open(config.md5_path, 'a', encoding="utf-8") as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str: str, encoding='utf-8'):
    '''将传入信息转化为md5字符串'''
    #字符串变为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)

    md5_obj = hashlib.md5()#md5对象
    md5_obj.update(str_bytes)#更新内容
    md5_hex = md5_obj.hexdigest()#md5的16进制字符串

    return md5_hex

class KnowledgeBASEService(object):#object是所有类的基类

    def __init__(self):
        #若文件夹不存在则创建
        os.makedirs(config.persist_directorty, exist_ok=True)
        self.chorma = Chroma(
            collection_name=config.collection_name,#数据库表名
            embedding_function=DashScopeEmbeddings(model = "text-embedding-v4"),#嵌入模型
            persist_directory=config.persist_directorty,#数据库本地文件
        ) #向量存储的实例 Chorma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,#分割后文本段长度上限
            chunk_overlap = config.chunk_overlap, #连续文本段之间字符重叠数量
            separators = config.separators,#自然段落划分用的符号
            length_function = len, #长度统计用的函数
        ) #文本分割器对象


    def upload_by_str(self, data, filename):
        '''将传入字符串嵌入成向量，然后存进向量数据库'''
        #先确定要不要去重
        md5_hex = get_string_md5(data)
        if check_md5(md5_str=md5_hex):
            return "[跳过已存在字符]"
        save_md5(md5_hex)

        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)#得到分割后的str的列表
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "xxx",
        }

        self.chorma.add_texts(#把内容加载到向量库中，因为chorma已经连接到数据库了
            #iterable -> list \ tuple
            knowledge_chunks,
            metadatas = [metadata for _ in knowledge_chunks],#字典类型，被包在列表中
        )

        return "[向量库更新完成]"

if __name__ == "__main__":
    service = KnowledgeBASEService()
    service.upload_by_str("周杰伦", "testfile")