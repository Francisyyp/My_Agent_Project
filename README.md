# My_Agent_Project: 智能财务调研 Agent 

本项目是一个从零构建的、具备工业级架构的智能财务 Agent。它经历了从基础 **ReAct** 到 **RAG (检索增强生成)**，再到使用 **LangGraph** 实现复杂状态管理和长期记忆的进化过程。

## 🌟 核心特性
- **推理引擎**: 基于 DeepSeek-V3 的 ReAct (Reason-Action) 循环。
- **本地知识库 (RAG)**: 集成 ChromaDB，支持针对英伟达 (NVIDIA) 等企业研报的语义检索。
- **长期记忆 (Persistence)**: 使用 LangGraph 的 SQLite 检查点机制，支持断点续传和多会话记忆。
- **工具链**: 包含实时股价查询、专业财务计算器及知识库检索工具。
- **可视化**: 自动生成 Agent 决策逻辑图 (`agent_graph.png`)。

## 📁 项目结构
- `01_Single_ReAct_Agent`: 基础 ReAct 逻辑手搓实现。
- `02_RAG_Agent`: 引入 ChromaDB 向量数据库实现知识库检索。
- `03_RAG_Memory_Agent`: 手搓 SQLite 实现的长期对话记忆。
- `04_LangGraph_Agent`: **[当前版本]** 使用 LangGraph 状态机重构，支持持久化。

## 🚀 快速启动 (以 04 模块为例)
```bash
cd 04_LangGraph_Agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
