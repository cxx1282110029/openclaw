#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音响应系统
将文字唤醒系统与语音输出结合
"""

import pyttsx3
import os
import tempfile
from pathlib import Path
import sys

class VoiceResponseSystem:
    """语音响应系统"""
    
    def __init__(self):
        self.engine = None
        self.output_dir = Path.home() / ".openclaw" / "voice_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.init_tts_engine()
    
    def init_tts_engine(self):
        """初始化TTS引擎"""
        try:
            self.engine = pyttsx3.init()
            
            # 获取可用语音
            voices = self.engine.getProperty('voices')
            print(f"找到 {len(voices)} 个语音引擎:")
            
            for i, voice in enumerate(voices):
                print(f"  [{i}] {voice.name} - {voice.languages}")
            
            # 尝试设置中文语音
            for voice in voices:
                if 'chinese' in voice.name.lower() or 'zh' in str(voice.languages).lower():
                    self.engine.setProperty('voice', voice.id)
                    print(f"设置中文语音: {voice.name}")
                    break
            
            # 设置参数
            self.engine.setProperty('rate', 180)  # 语速
            self.engine.setProperty('volume', 0.9)  # 音量
            
            return True
        except Exception as e:
            print(f"初始化TTS引擎失败: {e}")
            return False
    
    def text_to_speech(self, text: str, save_to_file: bool = True) -> str:
        """
        文本转语音
        
        Args:
            text: 要转换的文本
            save_to_file: 是否保存到文件
            
        Returns:
            音频文件路径（如果保存）或空字符串
        """
        if not self.engine:
            print("TTS引擎未初始化")
            return ""
        
        try:
            if save_to_file:
                # 生成文件名
                import hashlib
                import time
                text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
                timestamp = int(time.time())
                filename = f"tts_{timestamp}_{text_hash}.mp3"
                filepath = self.output_dir / filename
                
                # 保存到文件
                self.engine.save_to_file(text, str(filepath))
                self.engine.runAndWait()
                
                print(f"语音文件已保存: {filepath}")
                return str(filepath)
            else:
                # 直接播放
                self.engine.say(text)
                self.engine.runAndWait()
                return ""
                
        except Exception as e:
            print(f"文本转语音失败: {e}")
            return ""
    
    def get_wakeup_response(self, wakeup_word: str, mode: str = "professional") -> str:
        """获取唤醒响应文本"""
        responses = {
            "professional": {
                "龙虾": "贾维斯为您服务，请指示",
                "openclaw": "OpenClaw系统就绪，等待指令",
                "贾维斯": "您好，我是您的AI助手贾维斯",
                "一拳先生": "一拳先生在此，随时为您效劳"
            },
            "friendly": {
                "龙虾": "嘿，龙虾来啦！有什么需要帮忙的？",
                "openclaw": "OpenClaw在线，随时待命",
                "贾维斯": "贾维斯在此，请吩咐",
                "一拳先生": "一拳先生报到！今天想做什么？"
            },
            "technical": {
                "龙虾": "系统唤醒成功，所有功能正常",
                "openclaw": "OpenClaw核心系统启动完成",
                "贾维斯": "贾维斯AI引擎已激活",
                "一拳先生": "一拳先生服务进程运行中"
            }
        }
        
        mode_responses = responses.get(mode, responses["professional"])
        return mode_responses.get(wakeup_word, "系统已唤醒，请指示")
    
    def process_wakeup(self, wakeup_word: str, followup_text: str = "", mode: str = "professional"):
        """处理唤醒请求"""
        print(f"处理唤醒: {wakeup_word} (模式: {mode})")
        
        # 生成响应文本
        if followup_text:
            response_text = f"{self.get_wakeup_response(wakeup_word, mode)}。{followup_text}"
        else:
            response_text = self.get_wakeup_response(wakeup_word, mode)
        
        print(f"响应文本: {response_text}")
        
        # 转换为语音
        audio_file = self.text_to_speech(response_text, save_to_file=True)
        
        return {
            "wakeup_word": wakeup_word,
            "mode": mode,
            "response_text": response_text,
            "audio_file": audio_file,
            "success": bool(audio_file)
        }
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """清理旧的语音文件"""
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        deleted_count = 0
        for file in self.output_dir.glob("*.mp3"):
            try:
                file_age = current_time - file.stat().st_mtime
                if file_age > max_age_seconds:
                    file.unlink()
                    deleted_count += 1
            except:
                pass
        
        if deleted_count:
            print(f"清理了 {deleted_count} 个旧语音文件")


def main():
    """测试语音响应系统"""
    print("=" * 50)
    print("语音响应系统测试")
    print("=" * 50)
    
    system = VoiceResponseSystem()
    
    if not system.engine:
        print("无法初始化TTS引擎，退出测试")
        return
    
    # 测试用例
    test_cases = [
        ("龙虾", "", "professional"),
        ("openclaw", "帮我查一下今天的天气", "technical"),
        ("贾维斯", "设置下午3点的会议提醒", "professional"),
        ("一拳先生", "最近有什么新消息吗？", "friendly")
    ]
    
    for wakeup_word, followup, mode in test_cases:
        print(f"\n测试: {wakeup_word} + '{followup}' ({mode}模式)")
        result = system.process_wakeup(wakeup_word, followup, mode)
        
        if result["success"]:
            print(f"✅ 语音生成成功")
            print(f"   文件: {result['audio_file']}")
        else:
            print(f"❌ 语音生成失败")
    
    # 显示统计
    mp3_files = list(system.output_dir.glob("*.mp3"))
    print(f"\n语音文件目录: {system.output_dir}")
    print(f"当前语音文件数: {len(mp3_files)}")
    
    # 清理旧文件
    system.cleanup_old_files()


if __name__ == "__main__":
    main()