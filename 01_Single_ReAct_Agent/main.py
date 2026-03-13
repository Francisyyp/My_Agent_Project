import os
from openai import OpenAI
from dotenv import load_dotenv
from tools import search_price, calculator, tools_map
from utils import parse_action, save_log
from prompts import system_prompt

# 加载 .env 文件中的环境变量
load_dotenv()

# 初始化 DeepSeek 客户端（兼容 OpenAI 格式）
llm_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

# 封装一个简易的聊天函数，openai 这个包，chat_with_deepseek函数只是一个传输协议。
def chat_with_deepseek(messages):
    response = llm_client.chat.completions.create(
        model="deepseek-chat",  
        messages=messages,
        temperature=0.7, # 稍微给一点随机性
        stream=False,     # Agent 循环建议先用非流式，方便解析
        # 强制模型看到这个词就闭嘴，等待 Python 执行
        stop=["Observation:", "Observation"]
    )
    return response.choices[0].message.content

def run_agent(question):
    # 初始化记忆
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    for i in range(5):
        # 调用chat_with_deepseek，进行Reasoning
        content = chat_with_deepseek(messages) 
        print(f"\n--- [LOG] Round {i+1} 模型回复 ---\n{content}")
        
        # 判断过程
        if "Final Answer" in content:
            messages.append({"role": "assistant", "content": content})
            save_log(messages)
            return content
        
        # 数据流转，为Acting做准备
        action, action_input = parse_action(content)
        
        # Acting
        # --- 增加鲁棒性逻辑 ---
        if action and action in tools_map:
            try:
                # 执行工具并获得结果
                obs = tools_map[action](**action_input)
            except Exception as e:
                obs = f"工具执行报错: {str(e)}。请检查你的参数并重试。"
        elif action and action not in tools_map:
            obs = f"错误：工具 '{action}' 不存在。请从 [Search, Calculator] 中选择。"
        else:
            # 如果解析不到 Action，说明模型没按格式说话
            obs = "解析错误：未检测到正确的 Action 格式。请确保输出 'Action: [工具名]' 和 'Action Input: {JSON}'。"
        
        # 反馈 (Observation)
        print(f"👁️ [Observation]: {obs}")
        
        # 将本次推理和观察结果存入短期记忆
        messages.append({"role": "assistant", "content": content})
        messages.append({"role": "system", "content": f"Observation: {obs}"})
    
    save_log(messages)
    return "Agent 运行超过最大轮次，未得出结论。"


if __name__ == "__main__":
    user_query = "调研腾讯的股价，如果涨了10%，市值会变动多少？"
    run_agent(user_query)