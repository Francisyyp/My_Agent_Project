import re
import json

def parse_action(text):
    """
    改进版解析器：支持标准格式提取，也支持纯 JSON 块提取
    """
    # 1. 尝试标准格式提取 (ReAct 标准模式)
    action_match = re.search(r"Action:\s*(.*)", text)
    action_input_match = re.search(r"Action Input:\s*(\{.*\})", text, re.DOTALL) # DOTALL 处理多行 JSON

    if action_match and action_input_match:
        action = action_match.group(1).strip()
        try:
            action_input = json.loads(action_input_match.group(1).strip())
            return action, action_input
        except:
            pass # 如果标准模式解析 JSON 失败，进入下面的兜底逻辑

    # 2. 兜底逻辑：如果模型直接输出了 JSON 块（或者在 Markdown 代码块里）
    # 尝试在全文中寻找最外层的 {} 结构
    json_pattern = re.search(r"(\{.*\})", text, re.DOTALL)
    if json_pattern:
        try:
            data = json.loads(json_pattern.group(1).strip())
            
            # --- 启发式判断 Action ---
            # 如果 JSON 里有 company_name，我们就判定它是想 Search
            if "company_name" in data:
                return "Search", data
            # 如果 JSON 里有 price 或 k，我们就判定它是想 Calculator
            if "price" in data or "k" in data:
                # 兼容模型可能把 thought 写在 JSON 里的情况
                # 剔除掉无关字段，只保留函数需要的参数
                valid_params = {k: v for k, v in data.items() if k in ["price", "k"]}
                return "Calculator", valid_params
                
        except json.JSONDecodeError:
            return None, "JSON_ERROR"

    return None, None


def save_log(trajectory):
    """
    将对话轨迹存入 jsonl 文件
    """
    with open("agent_trace.jsonl", "a", encoding="utf-8") as f:
        # trajectory 通常就是你 main.py 里的 messages 列表
        f.write(json.dumps(trajectory, ensure_ascii=False) + "\n")