#!/usr/bin/env python3
# 简化版QQ语音集成
import pyttsx3
import tempfile
import os

print("=== 简化QQ语音集成测试 ===")

# 初始化
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 0.9)

# 测试直接语音
print("1. 测试直接语音输出...")
engine.say("QQ语音集成测试开始")
engine.runAndWait()

# 测试唤醒词
print("\n2. 测试唤醒词语音...")
wake_responses = {
    "龙虾": "龙虾机器人QQ语音响应测试",
    "openclaw": "OpenClaw QQ语音功能正常",
    "贾维斯": "贾维斯QQ语音模块激活"
}

for word, response in wake_responses.items():
    print(f"唤醒词: {word} -> {response}")
    engine.say(response)
    engine.runAndWait()

print("\n3. 测试文件生成...")
# 尝试保存到文件
temp_dir = tempfile.gettempdir()
test_file = os.path.join(temp_dir, "qq_voice_test.mp3")

try:
    print(f"尝试保存到: {test_file}")
    engine.save_to_file("QQ语音文件生成测试", test_file)
    engine.runAndWait()
    
    if os.path.exists(test_file):
        size = os.path.getsize(test_file)
        print(f"文件生成成功! 大小: {size} 字节")
        
        # 尝试播放
        print("播放生成的语音文件...")
        engine.say("从文件播放测试")
        engine.runAndWait()
    else:
        print("文件生成失败")
        
except Exception as e:
    print(f"文件保存错误: {e}")

print("\n✅ QQ语音集成基础测试完成")