from langchain_core.tools import tool
from retriever import VectorRetriever

retriever = VectorRetriever()

@tool
def search_price(company_name: str):
    """查询指定公司的实时股价。"""
    prices = {"英伟达": 250.0, "NVIDIA": 250.0, "腾讯": 380.0}
    return prices.get(company_name, 150.0)

@tool
def calculator(price: float, k: float):
    """财务计算器。用于计算市值变动。price为当前股价，k为涨跌幅小数。"""
    return float(price) * float(k) * 1000000

@tool
def knowledge_query(query: str):
    """【语义检索】查阅本地英伟达(NVIDIA)深度研报及历史财务表现。"""
    return retriever.search(query)

# 导出一个列表给 LangGraph 使用
tools = [search_price, calculator, knowledge_query]