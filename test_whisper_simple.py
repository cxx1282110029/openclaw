#!/usr/bin/env python3
# 简单Whisper测试
import sys
import tempfile
import os

print("测试Whisper语音识别")

try:
    import whisper
    print("Whisper导入成功")
    
    # 检查QQ语音文件
    qq_audio = r"C:\Users\Administrator\.openclaw\qqbot\downloads\65b66a8277dce336fd2792cf660d9c2d.bin"
    
    if os.path.exists(qq_audio):
        print(f"找到QQ语音文件: {qq_audio}")
        file_size = os.path.getsize(qq_audio)
        print(f"文件大小: {file_size} 字节")
        
        # 先复制到临时文件（避免修改原文件）
        import shutil
        temp_dir = tempfile.gettempdir()
        temp_audio = os.path.join(temp_dir, "qq_voice_test.wav")
        shutil.copy2(qq_audio, temp_audio)
        print(f"复制到临时文件: {temp_audio}")
        
        # 尝试使用Whisper识别
        print("\n加载Whisper模型...")
        print("注意：首次运行会下载模型文件")
        
        # 使用最小的模型测试
        model = whisper.load_model("tiny")
        print("模型加载成功")
        
        # 识别音频
        print("开始语音识别...")
        result = model.transcribe(temp_audio, language="zh")
        
        print("\n=== Whisper识别结果 ===")
        print(f"文本: {result['text']}")
        print(f"语言: {result['language']}")
        
        # 检查是否包含唤醒词
        wake_words = ["龙虾", "openclaw", "贾维斯"]
        text_lower = result['text'].lower()
        
        print("\n=== 唤醒词检测 ===")
        for word in wake_words:
            if word.lower() in text_lower:
                print(f"检测到唤醒词: {word}")
            else:
                print(f"未检测到: {word}")
                
        # 与QQ平台ASR对比
        print("\n=== 识别结果对比 ===")
        print(f"Whisper识别: {result['text']}")
        print(f"QQ平台ASR: '喂，龙虾你好。'")
        
        # 保存结果
        result_file = os.path.join(temp_dir, "whisper_result.txt")
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"音频文件: {qq_audio}\n")
            f.write(f"文件大小: {file_size} bytes\n")
            f.write(f"Whisper识别: {result['text']}\n")
            f.write(f"识别语言: {result['language']}\n")
            f.write(f"QQ平台ASR: 喂，龙虾你好。\n")
        
        print(f"\n结果已保存到: {result_file}")
        
    else:
        print("QQ语音文件不存在")
        print("创建测试音频...")
        
        # 创建测试音频
        import wave
        import struct
        import math
        
        temp_dir = tempfile.gettempdir()
        test_audio = os.path.join(temp_dir, "test_chinese.wav")
        
        sample_rate = 16000
        duration = 3
        num_samples = sample_rate * duration
        
        with wave.open(test_audio, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            # 生成包含"龙虾你好"的测试音频
            freq = 440
            for i in range(num_samples):
                # 简单的正弦波
                value = int(32767 * 0.5 * math.sin(2 * math.pi * freq * i / sample_rate))
                wav_file.writeframes(struct.pack('<h', value))
        
        print(f"创建测试文件: {test_audio}")
        
        # 测试识别
        model = whisper.load_model("tiny")
        result = model.transcribe(test_audio, language="zh")
        print(f"测试识别结果: {result['text']}")
        
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("\nWhisper测试完成")