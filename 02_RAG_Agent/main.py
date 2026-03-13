import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import tools_map, tools
from utils import save_log
from prompts import system_prompt

# 加载 .env 文件中的环境变量
load_dotenv()

# 初始化 DeepSeek 客户端（兼容 OpenAI 格式）
llm_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

def chat_with_deepseek(messages):
    """
    更新后的聊天函数，支持 tools 参数
    """
    response = llm_client.chat.completions.create(
        model="deepseek-chat",  
        messages=messages,
        tools=tools,         # 必须传入工具定义
        tool_choice="auto",  # 让模型决定是否用工具
        temperature=0.3,      # 做任务建议调低随机性
        stream=False,
        stop=["Observation:", "Observation", "Observe:"]
    )
    return response.choices[0].message



def run_agent(question):
    # 初始化记忆
    # 注意：在原生模式下，system_prompt 不需要教模型怎么写 Action 格式，只需要交待任务背景
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    for i in range(8):
        # 1. 获取模型回复
        message = chat_with_deepseek(messages) 
        
        # 2. 判断模型是想“说话”还是想“调工具”
        if not message.tool_calls:
            # 如果没有工具调用，说明给出了 Final Answer
            messages.append(message.model_dump())
            print(f"\n--- [LOG] Round {i+1} 最终回答 ---\n{message.content}")
            save_log(messages)
            return message.content
        
        # 3. 如果模型点单了（tool_calls），开始执行工具
        print(f"\n--- [LOG] Round {i+1} 模型发起工具调用 ---")
        
        # 必须先把模型“点单”的请求存入历史
        # messages.append(message)
        messages.append(message.model_dump()) # 将对象转换为字典
        
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            # 参数已经是解析好的 JSON 字符串了，转成字典即可
            args = json.loads(tool_call.function.arguments)
            
            print(f"🛠️  执行工具: {func_name} | 参数: {args}")
            
            try:
                # 从 tools_map 找到函数并执行
                if func_name in tools_map:
                    result = tools_map[func_name](**args)
                else:
                    result = f"错误：工具 {func_name} 未定义"
            except Exception as e:
                result = f"工具执行报错: {str(e)}"
            
            # 4. 把执行结果反馈给模型
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
            print(f"👁️  [Observation]: {str(result)[:25]}...") # 打印前100字缩略
            
    save_log(messages)
    return "Agent 运行超过最大轮次，未得出结论。"

if __name__ == "__main__":
    user_query = "先查询英伟达当前的股价。然后查阅本地研报，看看报告中提到的它在 2017 年的市场表现是怎样的？最后计算如果它的股价再涨 15%，市值变动是多少？"
    run_agent(user_query)