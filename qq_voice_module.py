#!/usr/bin/env python3
# QQ语音响应模块
import pyttsx3
import os
import tempfile

class QQVoiceResponse:
    def __init__(self):
        """初始化语音引擎"""
        self.engine = pyttsx3.init()
        self.setup_engine()
        
        # 临时目录用于保存语音文件
        self.temp_dir = tempfile.gettempdir()
        print(f"语音模块初始化完成，临时目录: {self.temp_dir}")
    
    def setup_engine(self):
        """配置语音引擎"""
        # 设置语音属性
        self.engine.setProperty('rate', 180)    # 语速
        self.engine.setProperty('volume', 0.9)  # 音量
        
        # 获取可用语音
        voices = self.engine.getProperty('voices')
        print(f"可用语音数量: {len(voices)}")
        
        # 尝试设置中文语音（如果可用）
        for voice in voices:
            if 'chinese' in voice.name.lower() or 'zh' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                print(f"使用中文语音: {voice.name}")
                break
    
    def text_to_speech(self, text, filename=None):
        """
        将文本转换为语音文件
        返回文件路径
        """
        if filename is None:
            # 生成唯一文件名
            import hashlib
            import time
            hash_str = hashlib.md5(text.encode()).hexdigest()[:8]
            filename = f"voice_{hash_str}_{int(time.time())}.mp3"
        
        filepath = os.path.join(self.temp_dir, filename)
        
        try:
            # 保存语音到文件
            self.engine.save_to_file(text, filepath)
            self.engine.runAndWait()
            
            # 检查文件是否生成
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                print(f"语音文件生成成功: {filepath} ({os.path.getsize(filepath)} bytes)")
                return filepath
            else:
                print("语音文件生成失败")
                return None
                
        except Exception as e:
            print(f"语音生成错误: {e}")
            return None
    
    def generate_wakeup_response(self, wake_word):
        """生成唤醒词响应语音"""
        responses = {
            "龙虾": "龙虾机器人已唤醒，贾维斯模式启动！",
            "openclaw": "OpenClaw 语音唤醒已激活，随时为您服务！",
            "贾维斯": "贾维斯在线，主人请吩咐！"
        }
        
        response_text = responses.get(wake_word, "语音唤醒已激活")
        filename = f"wakeup_{wake_word}.mp3"
        
        return self.text_to_speech(response_text, filename)
    
    def generate_qq_response(self, message_text):
        """根据QQ消息生成语音响应"""
        # 检查是否包含唤醒词
        wake_words = ["龙虾", "openclaw", "贾维斯"]
        text_lower = message_text.lower()
        
        for word in wake_words:
            if word.lower() in text_lower:
                print(f"检测到唤醒词: {word}")
                return self.generate_wakeup_response(word)
        
        # 普通响应
        response_text = f"收到消息: {message_text[:50]}..."
        return self.text_to_speech(response_text)
    
    def cleanup_old_files(self, max_age_hours=24):
        """清理旧的语音文件"""
        import time
        current_time = time.time()
        
        for filename in os.listdir(self.temp_dir):
            if filename.startswith("voice_") or filename.startswith("wakeup_"):
                filepath = os.path.join(self.temp_dir, filename)
                file_age = current_time - os.path.getmtime(filepath)
                
                if file_age > max_age_hours * 3600:  # 超过指定小时
                    try:
                        os.remove(filepath)
                        print(f"清理旧文件: {filename}")
                    except:
                        pass

# 测试函数
def test_qq_voice():
    print("=== QQ语音模块测试 ===")
    
    voice = QQVoiceResponse()
    
    # 测试1: 唤醒词响应
    print("\n1. 测试唤醒词响应...")
    wakeup_file = voice.generate_wakeup_response("龙虾")
    if wakeup_file:
        print(f"唤醒语音文件: {wakeup_file}")
    
    # 测试2: QQ消息响应
    print("\n2. 测试QQ消息响应...")
    test_messages = [
        "龙虾，今天天气怎么样？",
        "openclaw帮我查资料",
        "贾维斯启动任务模式",
        "普通消息测试"
    ]
    
    for msg in test_messages:
        print(f"\n消息: {msg}")
        voice_file = voice.generate_qq_response(msg)
        if voice_file:
            print(f"生成语音文件: {voice_file}")
    
    # 清理
    print("\n3. 清理测试文件...")
    voice.cleanup_old_files(max_age_hours=0)  # 立即清理
    
    print("\n✅ QQ语音模块测试完成！")

if __name__ == "__main__":
    test_qq_voice()