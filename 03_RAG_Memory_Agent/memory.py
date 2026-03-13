import sqlite3
import json
import os

class LongTermMemory:
    def __init__(self, db_path="03_RAG_Memory_Agent/agent_memory.db"):
        # 确保目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        # session_id 用来区分不同的对话，role 是角色，content 是文本，tool_calls 存 JSON 字符串
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                tool_calls TEXT,
                tool_call_id TEXT
            )
        ''')
        self.conn.commit()

    def save_message(self, session_id, message_dict):
        """将消息存入数据库，自动处理对象序列化"""
        cursor = self.conn.cursor()
        
        # 提取数据，如果是 tool_calls 对象则转为 JSON 字符串存储
        tool_calls = json.dumps(message_dict.get("tool_calls")) if message_dict.get("tool_calls") else None
        
        cursor.execute('''
            INSERT INTO chat_history (session_id, role, content, tool_calls, tool_call_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            session_id, 
            message_dict.get("role"), 
            message_dict.get("content"),
            tool_calls,
            message_dict.get("tool_call_id")
        ))
        self.conn.commit()

    def load_history(self, session_id, limit=50):
        """从数据库读取最近的 10 条对话记录"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT role, content, tool_calls, tool_call_id FROM chat_history 
            WHERE session_id = ? ORDER BY id DESC LIMIT ?
        ''', (session_id, limit))
        
        rows = cursor.fetchall()
        history = []
        # 因为读取是 DESC（倒序），我们要反转回来变成正序对话
        for row in reversed(rows):
            msg = {"role": row[0], "content": row[1]}
            if row[2]: msg["tool_calls"] = json.loads(row[2])
            if row[3]: msg["tool_call_id"] = row[3]
            history.append(msg)
        return history