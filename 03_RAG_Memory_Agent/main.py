import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import tools_map, tools
from utils import save_log
from prompts import system_prompt
from memory import LongTermMemory # <--- 导入你刚写的记忆模块

# 加载 .env 文件中的环境变量
load_dotenv()

# 初始化客户端
llm_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

# 初始化记忆总线
memory_bus = LongTermMemory()

def chat_with_deepseek(messages):
    response = llm_client.chat.completions.create(
        model="deepseek-chat",  
        messages=messages,
        tools=tools,         
        tool_choice="auto",  
        temperature=0.3,      
        stream=False,
        stop=["Observation:", "Observation", "Observe:"]
    )
    return response.choices[0].message

def run_agent(question, session_id="user_01"): # <--- 增加 session_id 以区分不同对话
    # 1. 【核心修改】启动时加载历史记忆
    history = memory_bus.load_history(session_id)
    
    if not history:
        # 如果是新对话，初始化 System Prompt
        messages = [{"role": "system", "content": system_prompt}]
    else:
        # 如果有历史，直接承接
        messages = history
    
    # 2. 【核心修改】将本次用户问题存入上下文并持久化到数据库
    user_msg = {"role": "user", "content": question}
    messages.append(user_msg)
    memory_bus.save_message(session_id, user_msg)
    
    for i in range(8):
        message = chat_with_deepseek(messages) 
        
        # 3. 【核心修改】记录模型的回复（无论是思考还是工具调用指令）
        msg_dict = message.model_dump()
        messages.append(msg_dict)
        memory_bus.save_message(session_id, msg_dict) # 存入数据库
        
        if not message.tool_calls:
            print(f"\n--- [LOG] Round {i+1} 最终回答 ---\n{message.content}")
            save_log(messages)
            return message.content
        
        print(f"\n--- [LOG] Round {i+1} 模型发起工具调用 ---")
        
        # 注意：这里你之前的代码有一行重复的 append(message.model_dump()) 我已经按上一轮建议帮你去掉了
        
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            print(f"🛠️  执行工具: {func_name} | 参数: {args}")
            
            try:
                if func_name in tools_map:
                    result = tools_map[func_name](**args)
                else:
                    result = f"错误：工具 {func_name} 未定义"
            except Exception as e:
                result = f"工具执行报错: {str(e)}"
            
            # 4. 【核心修改】将工具执行结果存入上下文并持久化
            obs_msg = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            }
            messages.append(obs_msg)
            memory_bus.save_message(session_id, obs_msg) # 存入数据库
            
            print(f"👁️  [Observation]: {str(result)[:25]}...") 
            
    save_log(messages)
    return "Agent 运行超过最大轮次，未得出结论。"

if __name__ == "__main__":
    # 固定一个 session_id，这样你这次聊天和下次聊天都会记在同一个“日记本”里
    current_session = "francis_test_01"
    
    print("🚀 财务 Agent 已上线！(输入 'exit' 或 'quit' 退出对话)")
    print(f"📌 当前会话 ID: {current_session}")
    print("-" * 50)

    while True:
        # 获取用户输入
        user_input = input("\n👤 用户: ")
        
        # 设置退出条件
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("👋 再见！期待下次为你服务。")
            break
        
        if not user_input.strip():
            continue

        # 执行 Agent 逻辑
        # 注意：这里我们传入了 session_id，确保记忆能对号入座
        try:
            run_agent(user_input, session_id=current_session)
        except Exception as e:
            print(f"❌ 运行出错: {e}")