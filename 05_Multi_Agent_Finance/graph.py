import sqlite3
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode  # <--- 新引入：专门负责执行工具的节点

# 导入你的协议和专家
from state import TeamState
from agents import (
    researcher_node, 
    charter_node, 
    consultant_node, 
    supervisor_node
)

# 导入所有工具，用于给 ToolNode 注册
# from tools.rag_tools import query_knowledge_base
# from tools.financial_tools import get_stock_price
# from tools.chart_tools import python_repl_tool
from tools import query_knowledge_base, get_stock_price, python_repl_tool

# --- 1. 定义工具节点 ---
# 把所有专家可能用到的工具都塞进去
tools = [query_knowledge_base, get_stock_price, python_repl_tool]
tool_node = ToolNode(tools)

# --- 2. 定义路由逻辑：判断是否需要执行工具 ---
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # 如果最后一条消息包含工具调用，就去 tools 节点
    if last_message.tool_calls:
        return "tools"
    # 否则，说明话已经说完了，回传给主管
    return "supervisor"

# --- 3. 构建图 ---
conn = sqlite3.connect("05_multi_agent_history.db", check_same_thread=False)
memory = SqliteSaver(conn)
workflow = StateGraph(TeamState)

# 添加节点
workflow.add_node("Researcher", researcher_node)
workflow.add_node("Charter", charter_node)
workflow.add_node("Consultant", consultant_node)
workflow.add_node("Supervisor", supervisor_node)
workflow.add_node("tools", tool_node) # <--- 添加工具执行节点

# --- 4. 重新连线 (核心变化) ---

# 当 Researcher 运行完，判断：是调工具还是回传主管？
workflow.add_conditional_edges(
    "Researcher",
    should_continue,
    {"tools": "tools", "supervisor": "Supervisor"}
)

# 当 Charter 运行完，同理
workflow.add_conditional_edges(
    "Charter",
    should_continue,
    {"tools": "tools", "supervisor": "Supervisor"}
)

# 工具节点执行完后，球该回传给谁？
# 这里有个技巧：工具执行完通常回传给“刚才要工具的那个人”
def post_tool_route(state):
    # 根据 state["sender"] 判断回给谁
    sender = state.get("sender")
    if sender == "Researcher":
        return "Researcher"
    return "Charter"

workflow.add_conditional_edges("tools", post_tool_route, {"Researcher": "Researcher", "Charter": "Charter"})

# 顾问和主管的逻辑保持简单
workflow.add_edge("Consultant", "Supervisor")

workflow.add_conditional_edges(
    "Supervisor",
    lambda x: x["next"],
    {
        "Researcher": "Researcher",
        "Charter": "Charter",
        "Consultant": "Consultant",
        "FINISH": END
    }
)

workflow.set_entry_point("Supervisor")
app = workflow.compile(checkpointer=memory)