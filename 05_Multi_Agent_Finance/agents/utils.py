import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_model():
    """统一获取配置好的 LLM 实例"""
    return ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        openai_api_base=os.getenv("DEEPSEEK_BASE_URL")
    )

def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    """创建一个带有系统提示词和工具的 Agent 节点。"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    # 绑定工具
    if tools:
        llm = llm.bind_tools(tools)
    return prompt | llm