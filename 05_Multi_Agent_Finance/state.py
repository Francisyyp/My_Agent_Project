from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class TeamState(TypedDict):
    # 1. messages: 核心对话流。
    # Annotated + add_messages 确保每个 Agent 的回复是“追加”到列表，而不是覆盖列表。
    messages: Annotated[List[BaseMessage], add_messages]
    
    # 2. next: 调度旗帜。
    # Supervisor 会修改这个字段，告诉 Graph 下一个该谁上场（比如 "Researcher" 或 "FINISH"）。
    next: str
    
    # 3. sender: 记录员。
    # 记录最后一次发言的 Agent 名字，方便调试和 Supervisor 判断进度。
    sender: str