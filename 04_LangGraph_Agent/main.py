import os
from dotenv import load_dotenv
from typing import Literal

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver

from state import AgentState
from tools import tools
from prompts import system_prompt

load_dotenv()

# 1. 初始化模型并绑定工具
llm = ChatOpenAI(
    model="deepseek-chat", 
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    temperature=0.3
)
# 将我们定义的 tools 列表告诉 LLM
llm_with_tools = llm.bind_tools(tools)

# 2. 定义节点 (Nodes)
def call_model(state: AgentState):
    """大脑节点：负责思考和决定动作"""
    # 如果是第一轮，加入 SystemMessage
    if not any(isinstance(m, SystemMessage) for m in state["messages"]):
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
    else:
        messages = state["messages"]
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 官方内置的工具执行节点，它会自动执行 state["messages"] 中最新的 tool_calls
tool_node = ToolNode(tools)

# 3. 定义连边逻辑 (Edges)
def should_continue(state: AgentState) -> Literal["tools", END]:
    """判断是去干活（tools）还是收工（END）"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 4. 组装图 (Workflow)
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent") # 工具执行完必须回传给模型继续思考

if __name__ == "__main__":
    # 配置存档位 ID
    config = {"configurable": {"thread_id": "francis_01"}}

    # 2. 使用 with 语句开启持久化连接
    # 如果想永久保存，请使用 "checkpoints.db"；如果只想临时测试，用 ":memory:"
    with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
        
        # 3. 在连接激活的状态下编译 app
        app = workflow.compile(checkpointer=checkpointer)
        
        # 4. 尝试生成架构图 (可选)
        try:
            # 这一步能让你看到神兵的“设计图”
            image_data = app.get_graph().draw_mermaid_png()
            with open("agent_graph.png", "wb") as f:
                f.write(image_data)
            print("🎨 架构图已保存至: agent_graph.png")
        except Exception as e:
            print(f"💡 架构图导出跳过 (如需导出请安装相关绘图库): {e}")

        print("🚀 LangGraph 财务 Agent 已上线！(输入 exit 退出)")
        print("-" * 50)

        while True:
            user_input = input("\n👤 用户: ")
            if user_input.lower() in ["exit", "quit", "退出"]:
                break
            
            # 5. 核心运行循环
            # 使用 stream_mode="values" 可以让我们在每一跳(Step)都拿到完整的状态
            for event in app.stream(
                {"messages": [("user", user_input)]}, 
                config=config,
                stream_mode="values"
            ):
                # 获取当前最新的消息
                if "messages" in event:
                    msg = event["messages"][-1]
                    # 过滤逻辑：只打印 AI 的文本回复
                    # 如果你想看工具调用的过程，可以把 msg.type == "tool" 也打印出来
                    if msg.type == "ai" and msg.content:
                        print(f"🤖 Agent: {msg.content}")