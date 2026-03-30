from agents.utils import get_model, create_agent
from langchain_openai import ChatOpenAI
from tools.rag_tools import query_knowledge_base
from tools.financial_tools import get_stock_price
from agents.prompts import RESEARCHER_PROMPT

llm = get_model()
# 研究员的专属装备
researcher_agent = create_agent(
    llm, 
    [query_knowledge_base, get_stock_price], 
    RESEARCHER_PROMPT
)

def researcher_node(state):
    # 调用 agent 并获取结果
    result = researcher_agent.invoke(state)
    return {
        "messages": [result],
        "sender": "Researcher"
    }