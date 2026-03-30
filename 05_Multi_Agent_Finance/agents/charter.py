from agents.utils import get_model, create_agent
from langchain_openai import ChatOpenAI
from tools.chart_tools import python_repl_tool
from agents.prompts import CHARTER_PROMPT

llm = get_model()
charter_agent = create_agent(
    llm, 
    [python_repl_tool], 
    CHARTER_PROMPT
)

def charter_node(state):
    result = charter_agent.invoke(state)
    return {
        "messages": [result],
        "sender": "Charter"
    }