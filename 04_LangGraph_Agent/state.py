from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # Annotated + add_messages 是关键：
    # 它告诉 LangGraph：每当产生新消息，请追加到列表末尾，而不是覆盖整个列表。
    messages: Annotated[list, add_messages]