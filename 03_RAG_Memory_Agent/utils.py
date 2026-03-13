import re
import json

def parse_action(text):
    """
    鲁棒解析器：即便模型不按 Action: 格式说话，只要有 JSON 就能救回来
    """
    # 1. 尝试标准 ReAct 格式
    action_match = re.search(r"Action:\s*(.*)", text)
    action_input_match = re.search(r"Action Input:\s*(\{.*\})", text, re.DOTALL)

    if action_match and action_input_match:
        try:
            return action_match.group(1).strip(), json.loads(action_input_match.group(1).strip())
        except:
            pass 

    # 2. 启发式：在全文中盲搜第一个 {} 结构
    json_pattern = re.search(r"(\{.*\})", text, re.DOTALL)
    if json_pattern:
        try:
            data = json.loads(json_pattern.group(1).strip())
            # 自动映射：如果 JSON 里有 query，一定是想查知识库
            if "query" in data: return "Knowledge_Query", data
            if "company_name" in data: return "Search", data
            if "price" in data or "k" in data: return "Calculator", data
        except:
            pass
            
    return None, None

def save_log(trajectory):
    with open("agent_trace.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(trajectory, ensure_ascii=False) + "\n")