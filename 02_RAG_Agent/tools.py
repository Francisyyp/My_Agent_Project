tools = [
    {
        "type": "function",
        "function": {
            "name": "Search",
            "description": "查询指定上市公司的实时股价。例如：查询英伟达当前的股价。",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {"type": "string", "description": "上市公司的官方名称或英文名，如 NVIDIA, 腾讯"}
                },
                "required": ["company_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Calculator",
            "description": "计算市值变动的具体金额。公式：股价 * 涨幅 * 100万股标准股本。",
            "parameters": {
                "type": "object",
                "properties": {
                    "price": {"type": "number", "description": "当前股价"},
                    "k": {"type": "number", "description": "涨幅小数，例如 10% 传 0.1"}
                },
                "required": ["price", "k"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Knowledge_Query",
            "description": "语义检索工具。用于查阅本地英伟达(NVIDIA)深度研报、财务历史、2017年表现等私有资料。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "具体的搜索关键词或问题描述"}
                },
                "required": ["query"]
            }
        }
    }
]

from retriever import VectorRetriever

# 初始化向量检索器
retriever = VectorRetriever()

def search_price(company_name):
    """查询实时股价 (目前为演示固定值)"""
    # 模拟真实场景：你可以这里接个爬虫或 API
    prices = {"英伟达": 250.0, "NVIDIA": 250.0, "腾讯": 380.0}
    return prices.get(company_name, 150.0)

def calculator(price, k):
    """计算市值变动"""
    return float(price) * float(k) * 1000000

def knowledge_query(query):
    """【语义检索】查阅本地英伟达(NVIDIA)深度研报"""
    return retriever.search(query)

tools_map = {
    "Search": search_price,
    "Calculator": calculator,
    "Knowledge_Query": knowledge_query
}