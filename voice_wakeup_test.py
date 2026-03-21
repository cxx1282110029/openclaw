#!/usr/bin/env python3
# 语音唤醒功能测试

import pyttsx3
import time

class VoiceWakeup:
    def __init__(self):
        print("初始化语音唤醒系统...")
        self.engine = pyttsx3.init()
        self.wake_words = ["龙虾", "openclaw", "贾维斯"]
        
        # 设置语音属性
        self.engine.setProperty('rate', 180)  # 语速
        self.engine.setProperty('volume', 0.9)  # 音量
        
        print(f"唤醒词设置: {self.wake_words}")
        print("语音唤醒系统就绪！")
    
    def speak(self, text):
        """语音输出"""
        print(f"[语音] {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def check_wake_word(self, text):
        """检查是否包含唤醒词"""
        text_lower = text.lower()
        for word in self.wake_words:
            if word.lower() in text_lower:
                return True, word
        return False, None
    
    def wakeup_response(self, wake_word):
        """唤醒响应"""
        responses = {
            "龙虾": "龙虾机器人已唤醒，贾维斯模式启动！",
            "openclaw": "OpenClaw 语音唤醒已激活，随时为您服务！",
            "贾维斯": "贾维斯在线，主人请吩咐！"
        }
        
        response = responses.get(wake_word, "语音唤醒已激活")
        self.speak(response)
        return response
    
    def test_all_wake_words(self):
        """测试所有唤醒词"""
        print("\n=== 唤醒词测试开始 ===")
        
        test_texts = [
            "你好龙虾，今天天气怎么样？",
            "openclaw，帮我查一下资料",
            "贾维斯，启动任务模式",
            "这个机器人真厉害",
            "龙虾变身贾维斯成功了"
        ]
        
        for text in test_texts:
            print(f"\n测试文本: {text}")
            detected, word = self.check_wake_word(text)
            if detected:
                print(f"✅ 检测到唤醒词: '{word}'")
                self.wakeup_response(word)
            else:
                print("❌ 未检测到唤醒词")
        
        print("\n=== 唤醒词测试完成 ===")

def main():
    # 创建语音唤醒实例
    wakeup = VoiceWakeup()
    
    # 测试唤醒功能
    print("\n正在测试语音唤醒功能...")
    
    # 测试1: 直接唤醒
    print("\n--- 测试1: 直接语音唤醒 ---")
    wakeup.speak("系统待机中，请说出唤醒词")
    time.sleep(1)
    
    # 模拟用户说出唤醒词
    test_input = "龙虾"
    print(f"\n用户输入: '{test_input}'")
    detected, word = wakeup.check_wake_word(test_input)
    if detected:
        print(f"🎯 成功检测到唤醒词: '{word}'")
        wakeup.wakeup_response(word)
    
    # 测试2: 完整测试
    print("\n--- 测试2: 唤醒词全面测试 ---")
    wakeup.test_all_wake_words()
    
    # 测试3: 语音反馈
    print("\n--- 测试3: 语音反馈测试 ---")
    wakeup.speak("语音唤醒功能测试完成")
    wakeup.speak("龙虾机器人已永久待命")
    wakeup.speak("随时响应您的指令")
    
    print("\n✅ 语音唤醒功能测试全部完成！")

if __name__ == "__main__":
    main()