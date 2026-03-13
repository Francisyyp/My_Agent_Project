import chromadb
from chromadb.utils import embedding_functions

class VectorRetriever:
    def __init__(self):
        # 连接到刚刚 ingest 好的数据库
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_collection(name="nvidia_knowledge", embedding_function=self.emb_fn)

    def search(self, query, top_k=5):
        """
        基于向量相似度的语义搜索
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            # 提取搜索到的文档内容
            documents = results['documents'][0]
            if not documents:
                return "在知识库中未找到相关语义内容。"
            return "\n---\n".join(documents)
        except Exception as e:
            return f"检索发生错误: {str(e)}"

if __name__ == "__main__":
    retriever = VectorRetriever()
    print(retriever.search("英伟达在2017年的业务增长点"))