from agents.utils import get_model,create_agent
from langchain_openai import ChatOpenAI
from agents.prompts import CONSULTANT_PROMPT

llm = get_model()
consultant_agent = create_agent(
    llm, 
    [], # 顾问通常不需要工具，他只负责思考
    CONSULTANT_PROMPT
)

def consultant_node(state):
    result = consultant_agent.invoke(state)
    return {
        "messages": [result],
        "sender": "Consultant"
    }