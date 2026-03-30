from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Literal
from agents.prompts import SUPERVISOR_PROMPT
from agents.utils import get_model, create_agent

# 定义主管的决策输出格式
class Router(BaseModel):
    next: Literal["Researcher", "Charter", "Consultant", "FINISH"]

def supervisor_node(state):
    llm = get_model()
    
    # 使用结构化输出（Structured Output）让主管只返回我们需要的 next 字段
    # structured_llm = llm.with_structured_output(Router)
    # 这会告诉 LangChain：别用什么 JSON Schema 了，用 DeepSeek 最稳的工具调用协议
    structured_llm = llm.with_structured_output(Router, method="function_calling")
    
    messages = [{"role": "system", "content": SUPERVISOR_PROMPT}] + state["messages"]
    result = structured_llm.invoke(messages)
    
    return {"next": result.next}