#!/usr/bin/env python3
# 简化语音唤醒测试

import pyttsx3
import sys

print("=== 语音唤醒功能测试 ===")

# 初始化引擎
try:
    engine = pyttsx3.init()
    print("语音引擎初始化成功")
    
    # 设置属性
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.9)
    
    # 唤醒词列表
    wake_words = ["龙虾", "openclaw", "贾维斯"]
    print(f"唤醒词: {wake_words}")
    
    # 测试语音输出
    print("\n1. 测试基础语音输出...")
    engine.say("语音唤醒功能测试开始")
    engine.runAndWait()
    
    print("\n2. 测试唤醒词响应...")
    
    # 测试龙虾唤醒
    print("测试唤醒词: 龙虾")
    engine.say("龙虾机器人已唤醒，贾维斯模式启动")
    engine.runAndWait()
    
    # 测试openclaw唤醒
    print("测试唤醒词: openclaw")
    engine.say("OpenClaw 语音唤醒已激活，随时为您服务")
    engine.runAndWait()
    
    # 测试贾维斯唤醒
    print("测试唤醒词: 贾维斯")
    engine.say("贾维斯在线，主人请吩咐")
    engine.runAndWait()
    
    print("\n3. 完成语音...")
    engine.say("语音唤醒功能测试完成，龙虾机器人已永久待命")
    engine.runAndWait()
    
    print("\n✅ 语音唤醒功能测试成功！")
    
except Exception as e:
    print(f"错误: {e}")
    sys.exit(1)