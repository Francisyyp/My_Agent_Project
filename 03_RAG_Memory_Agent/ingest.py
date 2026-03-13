import fitz  # PyMuPDF
import os
import chromadb
from chromadb.utils import embedding_functions

# 1. 初始化本地持久化向量数据库
# 会在 02_RAG_Agent 目录下生成一个 chroma_db 文件夹
client = chromadb.PersistentClient(path="02_RAG_Agent/chroma_db")
# 使用本地开源模型进行向量化（不需要联网，速度极快）
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="nvidia_knowledge", embedding_function=emb_fn)

def load_data(folder_path):
    all_text = ""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".pdf"):
            doc = fitz.open(file_path)
            for page in doc: all_text += page.get_text()
        elif file_name.endswith(".txt"):
            if "chunks_test" in file_name: continue
            with open(file_path, "r", encoding="utf-8") as f: all_text += f.read()
    return all_text

def chunk_text(text, chunk_size=600, overlap=100):
    cleaned_text = text.replace("\n", " ").replace("  ", " ")
    chunks = []
    start = 0
    while start < len(cleaned_text):
        end = start + chunk_size
        chunks.append(cleaned_text[start:end])
        start += (chunk_size - overlap)
    return chunks

if __name__ == "__main__":
    data_folder = "02_RAG_Agent/data"
    raw_content = load_data(data_folder)
    knowledge_chunks = chunk_text(raw_content)

    # 2. 【核心升级】将切片存入向量数据库
    ids = [f"id_{i}" for i in range(len(knowledge_chunks))]
    collection.add(
        documents=knowledge_chunks,
        ids=ids
    )
    
    # 同时保留一个 TXT 预览供你检查
    with open("02_RAG_Agent/data/chunks_test.txt", "w", encoding="utf-8") as f:
        for i, c in enumerate(knowledge_chunks):
            f.write(f"--- [块 {i}] ---\n{c}\n\n")
            
    print(f"✅ 工业级向量库已就绪！共存入 {len(knowledge_chunks)} 个切片。")