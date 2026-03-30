# My_Agent_Project: 智能财务调研 Agent (Intelligent Financial Research Agent)

> ⚠️ **项目研发状态声明 (Project Status & Roadmap)** > 本项目定位为持续演进的 Agentic Workflow 工程实践，旨在探索大型语言模型（LLM）在复杂金融投研场景下的落地范式。目前核心底层架构已完成由单体脚本向 **LangGraph 复杂状态机**的重构（迭代至 `04_LangGraph_Agent` 阶段）。
> 
> **后续规划**：`05` 模块及更高级的 **Multi-Agent 协作网络（包含 Supervisor 路由调度、审查者与执行者解耦等特性）** 正在高强度研发与架构设计中。本项目代码和文档库将伴随前沿智能体技术持续更新。

---

## 📖 项目愿景与架构概述 (Project Overview)

在真实世界的财务投研中，分析师需要处理海量的非结构化文本、进行动态的数据查询，并维持长周期的逻辑推理。本项目从零搭建了一个具备工业级雏形的智能财务 Agent，完整记录了智能体架构从**“基础提示词工程”**向**“具备图灵完备性质的图状态机”**跃迁的全过程。

系统以 DeepSeek-V3 为核心认知引擎，通过融合本地 RAG 知识库与外部 API 工具链，使 Agent 具备了从“阅读理解”到“量化计算”再到“得出投资逻辑”的全链路闭环能力。

---

## 🌟 核心技术特性 (Core Technical Features)

### 1. 认知与推理引擎 (Cognitive & Reasoning Engine)
- **DeepSeek-V3 驱动**: 深度适配其 Function Calling 与原生 ReAct (Reason-Act) 提示范式，实现高容错率的任务拆解、中间状态反思 (Observation) 与动态纠偏。
- **动态控制流**: 突破线性链式调用 (Chain) 的局限，允许 Agent 在遇到模糊指令时自主决定是“检索知识库”、“调用计算器”还是“向用户发起追问”。

### 2. 企业级检索引擎 (Enterprise-grade RAG Architecture)
- **向量化检索**: 底层集成 ChromaDB，针对英伟达 (NVIDIA) 等头部科技企业的长篇财报、10-K 文件及行业研报进行深度语义切片与 Embedding 向量化。
- **防幻觉机制**: 通过强制 Agent 在生成财务摘要时必须挂载 RAG 检索到的上下文 (Context)，严格抑制金融数据生成中的“幻觉 (Hallucination)”。

### 3. 全生命周期状态与记忆管理 (State & Memory Management)
- **LangGraph 状态机**: 摒弃传统数组形式的易失性 Message History，基于有向图 (DAG/Cyclic Graph) 对 Agent 的行为节点进行建模与状态流转。
- **SQLite Checkpoint 持久化**: 原生集成线程级 (Thread-level) 记忆管理。支持跨会话 (Multi-session) 的时间旅行 (Time Travel) 与断点续传，Agent 可以无缝回忆数天前的财报分析上下文。

### 4. 高扩展性工具链 (Extensible Toolchain)
- **Finance API 接入**: 实时对接外部金融数据接口，获取最新 TTM、市盈率及动态股价。
- **专有计算器**: 为财务比率、DCF 模型预估等提供具有确定性的沙盒计算工具。
- **可视化拓扑**: 运行时自动编译并导出 Agent 决策与路由的逻辑拓扑图 (`agent_graph.png`)，极大降低了复杂黑盒系统的调试成本。

---

## 📁 架构演进路线 (Architecture Roadmap)

本项目采用模块化分层递进的设计理念，每个子模块均可独立运行，代表了一个关键的架构里程碑：

### 🟢 阶段一：单体智能体基建
- **`01_Single_ReAct_Agent`**
  **[基础范式]** 剥离繁冗框架，纯代码手搓原生 ReAct 推理循环。验证了 LLM 在基础工具调度（Tool Use）上的可用性。

### 🟡 阶段二：外部知识增强
- **`02_RAG_Agent`**
  **[知识外挂]** 引入 ChromaDB 向量数据库。打通从 PDF 解析、文本 Chunking 到语义匹配的完整 RAG 流水线，解决模型垂直领域知识滞后的痛点。

### 🟠 阶段三：记忆与上下文固化
- **`03_RAG_Memory_Agent`**
  **[记忆重构]** 针对长轮次问答导致 token 溢出的问题，自主设计并实现基于 SQLite 的本地数据库，完成历史对话的持久化与滑动窗口截断。

### 🔴 阶段四：复杂图状态控制 (当前稳定版)
- **`04_LangGraph_Agent`**
  **[工业级重构]** 全面引入 LangGraph 接管核心控制流。将 Agent 的“思考”、“执行”、“检索”解耦为独立的图节点 (Nodes)，并配置严格的转移边 (Edges) 与条件路由 (Conditional Edges)。实现了高鲁棒性的复杂任务调度与原生 Checkpoint 持久化。

### 🟣 阶段五：分布式多智能体 (研发中)
- **`05_Multi_Agent_System`**
  **[🚧 施工中]** 下一代架构预留。计划演进为多角色协同工作流，包含：
  - `Supervisor`: 负责意图识别与任务分发。
  - `Data_Analyst`: 专职负责财报数据挖掘与计算。
  - `Market_Researcher`: 负责宏观新闻与研报的情感分析。
  - `Report_Writer`: 负责最终投研报告的整合与润色。

---

## 📄 许可证协议 (License)

本项目采用 [MIT License](LICENSE) 开源许可协议。欢迎开发者 Fork、提交 PR 并在投研场景中进行二次开发。