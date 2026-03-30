import os
from dotenv import load_dotenv

# 核心：这行必须放在所有 local import（比如 from graph import app）之前！
load_dotenv()

import uuid
from graph import app

def run_finance_team():
    # 1. 创建一个唯一的 thread_id，作为本次对话的“存档号”
    # 在实际应用中，你可以固定一个 ID（比如 "francis_001"）来延续昨天的对话
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    print("🚀 财务调研梦之队已就位！(输入 'exit' 退出)")
    print("-" * 50)

    while True:
        user_input = input("✨ Francis，你想调研哪家公司？\n>> ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👋 下次见！")
            break

        # 2. 调用指挥部 (app)
        # 我们使用 stream 模式，这样可以看到每个 Agent 思考的中间过程
        inputs = {"messages": [("user", user_input)]}
        
        for output in app.stream(inputs, config=config):
            # output 是一个字典，key 是节点名称，value 是该节点返回的更新
            for node_name, node_output in output.items():
                print(f"\n[{node_name}] 正在处理...")
                
                # 如果节点输出了消息，打印出它的回复内容
                if "messages" in node_output:
                    last_msg = node_output["messages"][-1]
                    # 因为节点可能产生多条消息，我们只想看它最后定稿的那一句
                    print(f"🤖 内容: {last_msg.content[:20]}...") # 打印前200字
                
                # 如果主管更新了“下一位”是谁
                if "next" in node_output:
                    print(f"📍 主管指派下一步: {node_output['next']}")

        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    run_finance_team()