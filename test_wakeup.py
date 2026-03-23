#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版唤醒系统测试
"""

import re
import json
from datetime import datetime

class SimpleWakeupSystem:
    def __init__(self):
        self.wakeup_words = {
            "龙虾": {"priority": 10, "mode": "professional"},
            "openclaw": {"priority": 9, "mode": "technical"},
            "贾维斯": {"priority": 8, "mode": "assistant"},
            "一拳先生": {"priority": 7, "mode": "friendly"}
        }
    
    def detect(self, text):
        text_lower = text.lower().strip()
        
        for word, info in self.wakeup_words.items():
            pattern = r'\b' + re.escape(word.lower()) + r'\b'
            if re.search(pattern, text_lower):
                return True, word, info
        
        return False, None, None

def main():
    system = SimpleWakeupSystem()
    
    test_cases = [
        "龙虾，今天天气怎么样？",
        "openclaw，帮我查一下资料",
        "贾维斯，设置一个提醒",
        "一拳先生，有什么新消息吗？",
        "普通对话，没有唤醒词"
    ]
    
    print("=" * 40)
    print("唤醒系统测试")
    print("=" * 40)
    
    for test in test_cases:
        print(f"\n输入: {test}")
        detected, word, info = system.detect(test)
        
        if detected:
            print(f"[检测到] 唤醒词: {word}")
            print(f"        模式: {info['mode']}")
            print(f"        优先级: {info['priority']}")
            
            # 提取后续内容
            followup = test.replace(word, "").strip(" ，。!?")
            if followup:
                print(f"        后续内容: {followup}")
        else:
            print("[未检测] 无唤醒词")

if __name__ == "__main__":
    main()