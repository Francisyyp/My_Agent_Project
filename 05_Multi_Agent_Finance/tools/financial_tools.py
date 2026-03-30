from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

@tool
def get_stock_price(ticker: str):
    """获取指定股票的当前价格。"""
    # 实际项目中这里会接入 yfinance 或 alpha_vantage
    return f"{ticker} 的当前价格是 $185.20 (模拟数据)"

# 如果你有 Tavily API Key，可以用这个，没有的话先注释掉
# search = TavilySearchResults(max_results=3)