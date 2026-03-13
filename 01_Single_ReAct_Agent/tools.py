import random

def search_price(company_name):
    """模拟查询股价"""
    # 使用变量作为 Key，并返回浮点数
    price = round(random.uniform(100.0, 500.0), 2)
    return price

def calculator(price, k):
    """计算市值变化：100万股 * 价格 * 涨幅"""
    # 确保输入是数字
    return float(price) * float(k) * 1000000

# 核心：将字符串名称映射到真实的 Python 函数
# 这样你的主循环看到 "Action: Search" 才知道去调哪个函数
tools_map = {
    "Search": search_price,
    "Calculator": calculator
}