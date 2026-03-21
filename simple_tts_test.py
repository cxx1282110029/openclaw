#!/usr/bin/env python3
# Windows TTS 简单测试

import sys

print("测试Windows语音功能...")

# 尝试使用pyttsx3库
try:
    import pyttsx3
    print("找到pyttsx3库，尝试初始化...")
    
    # 初始化引擎
    engine = pyttsx3.init()
    
    # 测试中文（如果支持）
    print("测试中文语音...")
    engine.say("龙虾机器人已启动")
    engine.runAndWait()
    
    # 测试英文
    print("测试英文语音...")
    engine.say("OpenClaw voice wakeup enabled")
    engine.runAndWait()
    
    print("语音测试成功！")
    
except ImportError:
    print("未安装pyttsx3库")
    print("安装命令: pip install pyttsx3")
    
except Exception as e:
    print(f"语音测试失败: {e}")
    print("可能的原因:")
    print("1. 没有可用的语音引擎")
    print("2. 权限问题")
    print("3. 系统语音功能被禁用")