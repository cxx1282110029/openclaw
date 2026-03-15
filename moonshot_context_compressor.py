"""
Moonshot API 上下文压缩工具
减少多轮对话的 token 消耗
"""

from openai import OpenAI
from typing import List, Dict, Any
import json

class MoonshotContextCompressor:
    """Moonshot 上下文压缩器 - 自动总结历史消息"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.moonshot.cn/v1"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.summary_model = "moonshot-v1-8k"  # 便宜的模型做总结
        self.main_model = "moonshot-v1-32k"    # 主力模型
        
    def compress_messages(
        self, 
        messages: List[Dict[str, str]], 
        threshold: int = 6,  # 超过6条消息开始压缩
        keep_recent: int = 2  # 保留最近2条原消息
    ) -> List[Dict[str, str]]:
        """
        压缩消息历史
        
        Args:
            messages: 原始消息列表
            threshold: 触发压缩的阈值（消息数）
            keep_recent: 保留最近几条不压缩
        
        Returns:
            压缩后的消息列表
        """
        if len(messages) <= threshold:
            return messages
        
        # 系统提示词始终保留
        system_msg = None
        if messages and messages[0].get("role") == "system":
            system_msg = messages[0]
            messages = messages[1:]
        
        # 分割：需要总结的部分 + 保留的部分
        to_summarize = messages[:-keep_recent] if keep_recent > 0 else messages
        to_keep = messages[-keep_recent:] if keep_recent > 0 else []
        
        # 生成总结
        summary = self._generate_summary(to_summarize)
        
        # 组装新消息列表
        result = []
        if system_msg:
            result.append(system_msg)
        
        result.append({
            "role": "system",
            "content": f"【前文总结】{summary}"
        })
        
        result.extend(to_keep)
        
        return result
    
    def _generate_summary(self, messages: List[Dict[str, str]]) -> str:
        """用便宜模型生成消息总结"""
        
        summary_prompt = """请简洁总结以下对话的关键信息（100字以内）：

对话内容：
"""
        for msg in messages:
            role = "用户" if msg["role"] == "user" else "助手"
            summary_prompt += f"{role}: {msg['content'][:200]}...\n"
        
        try:
            response = self.client.chat.completions.create(
                model=self.summary_model,
                messages=[
                    {"role": "system", "content": "你是一个对话总结助手，请提取关键信息，不要遗漏重要事实、数据或决定。"},
                    {"role": "user", "content": summary_prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            # 总结失败时，截断处理
            return f"（前文过长已截断）最后提到：{messages[-1]['content'][:100]}..."
    
    def chat_with_compression(
        self, 
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Any:
        """
        带自动压缩的对话
        
        使用示例：
            compressor = MoonshotContextCompressor(api_key="your-key")
            
            messages = [
                {"role": "system", "content": "你是一个股票分析助手"},
                {"role": "user", "content": "分析茅台股票"},
                {"role": "assistant", "content": "茅台当前价格..."},
                # ... 更多对话
            ]
            
            response = compressor.chat_with_compression(messages)
        """
        # 压缩消息
        compressed = self.compress_messages(messages)
        
        # 打印压缩效果
        orig_tokens = self._estimate_tokens(messages)
        new_tokens = self._estimate_tokens(compressed)
        print(f"📦 上下文压缩: {len(messages)}条 → {len(compressed)}条 | 约 {orig_tokens} → {new_tokens} tokens")
        
        # 调用主模型
        response = self.client.chat.completions.create(
            model=self.main_model,
            messages=compressed,
            **kwargs
        )
        
        return response
    
    def _estimate_tokens(self, messages: List[Dict[str, str]]) -> int:
        """粗略估算 token 数（中文约1字=1token）"""
        total = 0
        for msg in messages:
            total += len(msg.get("content", ""))
        return total


# ============ 使用示例 ============

if __name__ == "__main__":
    # 初始化
    compressor = MoonshotContextCompressor(
        api_key="your-moonshot-api-key"
    )
    
    # 模拟长对话
    long_conversation = [
        {"role": "system", "content": "你是一个专业的编程助手"},
        {"role": "user", "content": "教我 Python"},
        {"role": "assistant", "content": "Python 是一种高级编程语言..."},
        {"role": "user", "content": "怎么定义函数？"},
        {"role": "assistant", "content": "用 def 关键字..."},
        {"role": "user", "content": "那类呢？"},
        {"role": "assistant", "content": "用 class 关键字..."},
        {"role": "user", "content": "给我写个例子"},
        {"role": "assistant", "content": "```python\nclass Dog:\n    def __init__(self):..."},
        {"role": "user", "content": "现在问股票分析"},
        {"role": "assistant", "content": "股票分析需要..."},
    ]
    
    # 使用压缩功能
    response = compressor.chat_with_compression(
        long_conversation,
        stream=False,
        temperature=0.7
    )
    
    print(f"\n回答: {response.choices[0].message.content}")


# ============ 进阶：带缓存的会话管理 ============

class SmartChatSession:
    """智能会话管理 - 自动压缩 + Token 预算控制"""
    
    def __init__(self, api_key: str, max_tokens_budget: int = 8000):
        self.compressor = MoonshotContextCompressor(api_key)
        self.messages = []
        self.max_budget = max_tokens_budget
        
    def add_message(self, role: str, content: str):
        """添加消息"""
        self.messages.append({"role": role, "content": content})
        
    def send(self, user_message: str, **kwargs) -> str:
        """发送消息并获取回复"""
        self.add_message("user", user_message)
        
        # 检查是否超出预算，需要压缩
        current_tokens = self.compressor._estimate_tokens(self.messages)
        if current_tokens > self.max_budget * 0.8:  # 达到80%预算
            print(f"⚠️ 接近 Token 预算 ({current_tokens}/{self.max_budget})，触发压缩")
        
        response = self.compressor.chat_with_compression(self.messages, **kwargs)
        reply = response.choices[0].message.content
        
        self.add_message("assistant", reply)
        return reply
    
    def clear(self):
        """清空对话（保留系统提示）"""
        system = self.messages[0] if self.messages and self.messages[0].get("role") == "system" else None
        self.messages = [system] if system else []


"""
使用 SmartChatSession 更简单：

session = SmartChatSession(api_key="xxx", max_tokens_budget=10000)

# 第一次调用（无压缩）
reply1 = session.send("讲个故事")

# 第 N 次调用（自动压缩历史）
reply2 = session.send("然后发生了什么？")
reply3 = session.send("主角最后怎么了？")
# ... 长对话会自动压缩，省钱！
"""
