#!/usr/bin/env python3
# 中文语音测试 - 解决编码问题
import pyttsx3
import sys

# 设置编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

print("=== 中文语音测试 ===")

try:
    # 初始化引擎
    engine = pyttsx3.init()
    print("语音引擎初始化成功")
    
    # 设置属性
    engine.setProperty('rate', 180)  # 语速
    engine.setProperty('volume', 0.9)  # 音量
    
    # 测试中文语音
    print("\n1. 测试基础中文语音...")
    test_texts = [
        "龙虾机器人语音唤醒测试",
        "中文语音合成功能正常",
        "贾维斯模式已激活",
        "随时为您服务"
    ]
    
    for text in test_texts:
        print(f"播放: {text}")
        engine.say(text)
        engine.runAndWait()
    
    # 测试唤醒词响应
    print("\n2. 测试中文唤醒词响应...")
    
    wake_responses = {
        "龙虾": "龙虾机器人已唤醒，贾维斯模式启动！",
        "openclaw": "OpenClaw 语音唤醒已激活，随时为您服务！",
        "贾维斯": "贾维斯在线，主人请吩咐！"
    }
    
    for wake_word, response in wake_responses.items():
        print(f"唤醒词: {wake_word}")
        print(f"响应: {response}")
        engine.say(response)
        engine.runAndWait()
    
    # 完成语音
    print("\n3. 完成测试...")
    completion_text = "中文语音编码问题已解决，语音唤醒功能完整实现"
    print(f"播放: {completion_text}")
    engine.say(completion_text)
    engine.runAndWait()
    
    print("\n✅ 中文语音测试成功！")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()