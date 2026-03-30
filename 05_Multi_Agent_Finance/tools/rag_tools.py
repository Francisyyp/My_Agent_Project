import chromadb
from chromadb.utils import embedding_functions
from langchain_core.tools import tool

# 1. 这一部分就是你 04 里的逻辑，直接写在文件顶层，保证工具初始化时就连上数据库
client = chromadb.PersistentClient(path="chroma_db")
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
# 获取你在 04 里建好的 collection
collection = client.get_collection(name="nvidia_knowledge", embedding_function=emb_fn)

@tool
def query_knowledge_base(query: str):
    """
    当你需要查询英伟达财报、业务增长点或内部研究报告时，调用此工具。
    输入应该是具体的查询问题。
    """
    try:
        results = collection.query(query_texts=[query], n_results=5)
        documents = results['documents'][0]
        if not documents:
            return "在知识库中未找到相关内容。"
        return "\n---\n".join(documents)
    except Exception as e:
        return f"检索发生错误: {str(e)}"