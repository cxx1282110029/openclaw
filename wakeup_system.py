#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 文字唤醒系统
版本: 1.0.0
作者: 一拳先生
日期: 2026-03-23

功能:
1. 关键词唤醒检测
2. 优先级响应处理
3. 唤醒历史记录
4. 响应模式切换
"""

import re
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class TextWakeupSystem:
    """文字唤醒系统"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.wakeup_words = {
            "龙虾": {
                "priority": 10,
                "response_mode": "professional",
                "description": "主要唤醒词"
            },
            "openclaw": {
                "priority": 9,
                "response_mode": "technical",
                "description": "英文唤醒词"
            },
            "贾维斯": {
                "priority": 8,
                "response_mode": "assistant",
                "description": "角色唤醒词"
            },
            "一拳先生": {
                "priority": 7,
                "response_mode": "friendly",
                "description": "名称唤醒词"
            },
            "hey": {
                "priority": 6,
                "response_mode": "casual",
                "description": "轻松唤醒词"
            },
            "喂": {
                "priority": 5,
                "response_mode": "direct",
                "description": "直接唤醒词"
            }
        }
        
        self.response_modes = {
            "professional": {
                "style": "专业、简洁、高效",
                "emoji": "👔",
                "greeting": "贾维斯为您服务"
            },
            "technical": {
                "style": "技术导向、详细",
                "emoji": "💻",
                "greeting": "OpenClaw系统就绪"
            },
            "assistant": {
                "style": "贴心、主动、周到",
                "emoji": "🤖",
                "greeting": "您好，我是您的AI助手"
            },
            "friendly": {
                "style": "友好、亲切",
                "emoji": "👊",
                "greeting": "一拳先生在此！"
            },
            "casual": {
                "style": "轻松、随意",
                "emoji": "😊",
                "greeting": "嘿，有什么需要帮忙的？"
            },
            "direct": {
                "style": "直接、快速",
                "emoji": "⚡",
                "greeting": "请讲"
            }
        }
        
        # 历史记录
        self.history_file = Path.home() / ".openclaw" / "wakeup_history.json"
        self.history_file.parent.mkdir(exist_ok=True)
        
        # 加载配置
        if config_path:
            self.load_config(config_path)
        
        # 初始化历史记录
        self.wakeup_history = self.load_history()
    
    def detect_wakeup(self, text: str) -> Tuple[bool, Optional[Dict]]:
        """
        检测文本中是否包含唤醒词
        
        Args:
            text: 输入的文本
            
        Returns:
            Tuple[是否唤醒, 唤醒词信息]
        """
        text_lower = text.lower().strip()
        
        # 检查每个唤醒词
        detected_words = []
        for word, info in self.wakeup_words.items():
            pattern = r'\b' + re.escape(word.lower()) + r'\b'
            if re.search(pattern, text_lower):
                detected_words.append((word, info))
        
        if not detected_words:
            return False, None
        
        # 选择优先级最高的唤醒词
        detected_words.sort(key=lambda x: x[1]['priority'], reverse=True)
        best_word, best_info = detected_words[0]
        
        # 记录唤醒历史
        self.record_wakeup(best_word, text)
        
        return True, {
            "word": best_word,
            "info": best_info,
            "response_mode": best_info["response_mode"],
            "timestamp": datetime.now().isoformat(),
            "original_text": text
        }
    
    def get_response(self, wakeup_info: Dict, followup_text: str = "") -> Dict:
        """
        获取唤醒响应
        
        Args:
            wakeup_info: 唤醒词信息
            followup_text: 后续文本
            
        Returns:
            响应信息字典
        """
        mode = wakeup_info["response_mode"]
        mode_info = self.response_modes[mode]
        word = wakeup_info["word"]
        
        # 基础响应
        response = {
            "greeting": f"{mode_info['emoji']} {mode_info['greeting']}",
            "style": mode_info["style"],
            "mode": mode,
            "wakeup_word": word,
            "timestamp": datetime.now().isoformat(),
            "priority": self.wakeup_words[word]["priority"]
        }
        
        # 如果有后续文本，添加处理建议
        if followup_text:
            response["followup"] = followup_text
            response["action"] = self._analyze_followup(followup_text)
        
        return response
    
    def _analyze_followup(self, text: str) -> str:
        """分析后续文本的意图"""
        text_lower = text.lower()
        
        # 简单意图识别
        if any(word in text_lower for word in ["帮助", "help", "怎么", "如何"]):
            return "提供帮助"
        elif any(word in text_lower for word in ["天气", "weather"]):
            return "查询天气"
        elif any(word in text_lower for word in ["时间", "几点", "time"]):
            return "提供时间"
        elif any(word in text_lower for word in ["提醒", "提醒我", "remind"]):
            return "设置提醒"
        elif any(word in text_lower for word in ["计划", "任务", "todo"]):
            return "任务管理"
        elif any(word in text_lower for word in ["文件", "文档", "file"]):
            return "文件操作"
        elif any(word in text_lower for word in ["搜索", "查找", "search"]):
            return "搜索信息"
        else:
            return "常规对话"
    
    def record_wakeup(self, word: str, context: str):
        """记录唤醒历史"""
        record = {
            "word": word,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "priority": self.wakeup_words[word]["priority"],
            "mode": self.wakeup_words[word]["response_mode"]
        }
        
        self.wakeup_history.append(record)
        
        # 只保留最近100条记录
        if len(self.wakeup_history) > 100:
            self.wakeup_history = self.wakeup_history[-100:]
        
        self.save_history()
    
    def load_history(self) -> List[Dict]:
        """加载唤醒历史"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """保存唤醒历史"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.wakeup_history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def load_config(self, config_path: str):
        """加载配置文件"""
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if "wakeup_words" in config:
                        self.wakeup_words.update(config["wakeup_words"])
                    if "response_modes" in config:
                        self.response_modes.update(config["response_modes"])
            except:
                pass
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self.wakeup_history:
            return {"total": 0, "by_word": {}, "by_mode": {}}
        
        total = len(self.wakeup_history)
        by_word = {}
        by_mode = {}
        
        for record in self.wakeup_history:
            word = record["word"]
            mode = record["mode"]
            
            by_word[word] = by_word.get(word, 0) + 1
            by_mode[mode] = by_mode.get(mode, 0) + 1
        
        # 最近24小时
        recent_24h = 0
        day_ago = datetime.now().timestamp() - 86400
        
        for record in self.wakeup_history:
            try:
                record_time = datetime.fromisoformat(record["timestamp"]).timestamp()
                if record_time > day_ago:
                    recent_24h += 1
            except:
                pass
        
        return {
            "total": total,
            "recent_24h": recent_24h,
            "by_word": by_word,
            "by_mode": by_mode,
            "most_used_word": max(by_word.items(), key=lambda x: x[1])[0] if by_word else None,
            "most_used_mode": max(by_mode.items(), key=lambda x: x[1])[0] if by_mode else None
        }
    
    def add_wakeup_word(self, word: str, priority: int = 5, 
                       response_mode: str = "assistant", 
                       description: str = "自定义唤醒词"):
        """添加自定义唤醒词"""
        self.wakeup_words[word] = {
            "priority": priority,
            "response_mode": response_mode,
            "description": description
        }
    
    def remove_wakeup_word(self, word: str):
        """移除唤醒词"""
        if word in self.wakeup_words:
            del self.wakeup_words[word]


# 使用示例
def main():
    """测试唤醒系统"""
    system = TextWakeupSystem()
    
    # 测试用例
    test_cases = [
        "龙虾，今天天气怎么样？",
        "openclaw，帮我查一下资料",
        "贾维斯，设置一个提醒",
        "一拳先生，有什么新消息吗？",
        "hey，最近怎么样？",
        "喂，在吗？",
        "普通对话，没有唤醒词"
    ]
    
    print("=" * 50)
    print("文字唤醒系统测试")
    print("=" * 50)
    
    for test in test_cases:
        print(f"\n输入: {test}")
        is_wakeup, info = system.detect_wakeup(test)
        
        if is_wakeup:
            # 提取后续文本（如果有）
            followup = test.replace(info["word"], "").strip(" ，。!?")
            response = system.get_response(info, followup)
            
            print(f"[OK] 检测到唤醒词: {info['word']}")
            print(f"   响应模式: {response['mode']} ({response['style']})")
            print(f"   问候语: {response['greeting']}")
            if 'action' in response:
                print(f"   建议操作: {response['action']}")
        else:
            print("[NO] 未检测到唤醒词")
    
    # 显示统计
    stats = system.get_stats()
    print(f"\n{'='*50}")
    print("系统统计:")
    print(f"  总唤醒次数: {stats['total']}")
    print(f"  最近24小时: {stats['recent_24h']}")
    if stats['most_used_word']:
        print(f"  最常用唤醒词: {stats['most_used_word']}")
    if stats['most_used_mode']:
        print(f"  最常用模式: {stats['most_used_mode']}")


if __name__ == "__main__":
    main()