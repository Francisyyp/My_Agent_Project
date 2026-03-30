import os

# 定义项目根目录名称
project_name = "05_Multi_Agent_Finance"

# 定义需要创建的文件夹结构
folders = [
    f"{project_name}/agents",
    f"{project_name}/tools",
    f"{project_name}/data",      # 存放研报 PDF
    f"{project_name}/chroma_db"  # 存放向量数据库
]

# 定义需要预创建的空文件
files = [
    f"{project_name}/.env",
    f"{project_name}/requirements.txt",
    f"{project_name}/state.py",
    f"{project_name}/graph.py",
    f"{project_name}/main.py",
    f"{project_name}/agents/__init__.py",
    f"{project_name}/agents/researcher.py",
    f"{project_name}/agents/charter.py",
    f"{project_name}/agents/consultant.py",
    f"{project_name}/agents/supervisor.py",
    f"{project_name}/tools/__init__.py",
    f"{project_name}/tools/financial_tools.py",
    f"{project_name}/tools/rag_tools.py",
    f"{project_name}/tools/chart_tools.py",
]

def setup():
    # 1. 创建文件夹
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 已创建文件夹: {folder}")

    # 2. 创建空文件
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w', encoding='utf-8') as f:
                # 给 requirements.txt 预填一些内容
                if "requirements.txt" in file:
                    f.write("langchain\nlangchain-openai\nlangchain-community\nlanggraph\nlanggraph-checkpoint-sqlite\nchromadb\nsentence-transformers\npandas\nmatplotlib\nlangchain-experimental\npython-dotenv\n")
            print(f"📄 已创建文件: {file}")

if __name__ == "__main__":
    setup()
    print("\n✅ 项目结构初始化完成！")