#!/usr/bin/env python3
# 生成语音唤醒响应文件
import pyttsx3
import tempfile
import os

def generate_wakeup_response():
    print("=== 生成语音唤醒响应 ===")
    
    # 初始化语音引擎
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.9)
    
    # 创建响应文本
    response_text = "龙虾你好！语音唤醒功能测试成功，贾维斯模式已激活，随时为您服务！"
    
    print(f"响应文本: {response_text}")
    
    # 生成语音文件
    temp_dir = tempfile.gettempdir()
    output_file = os.path.join(temp_dir, "lobster_wakeup_response.mp3")
    
    try:
        print(f"生成语音文件: {output_file}")
        engine.save_to_file(response_text, output_file)
        engine.runAndWait()
        
        # 检查文件
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"语音文件生成成功！大小: {file_size} 字节")
            print(f"文件路径: {output_file}")
            
            # 测试播放一小段
            print("测试播放...")
            engine.say("语音响应生成完成")
            engine.runAndWait()
            
            return output_file
        else:
            print("文件生成失败")
            return None
            
    except Exception as e:
        print(f"错误: {e}")
        return None

if __name__ == "__main__":
    result = generate_wakeup_response()
    if result:
        print(f"\n语音文件已生成: {result}")