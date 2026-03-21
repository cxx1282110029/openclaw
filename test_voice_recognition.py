#!/usr/bin/env python3
# 语音识别测试脚本
import os
import tempfile
import sys

print("=== 语音识别准确率优化测试 ===")

# 测试文件路径（模拟QQ下载的语音文件）
test_audio_path = r"C:\Users\Administrator\.openclaw\qqbot\downloads\65b66a8277dce336fd2792cf660d9c2d.bin"

print(f"测试音频文件: {test_audio_path}")

# 检查文件是否存在
if os.path.exists(test_audio_path):
    file_size = os.path.getsize(test_audio_path)
    print(f"✅ 音频文件存在，大小: {file_size} 字节")
    
    # 检查文件类型
    with open(test_audio_path, 'rb') as f:
        header = f.read(4)
        print(f"文件头: {header.hex()}")
        
        # 常见音频文件头
        audio_signatures = {
            b'RIFF': 'WAV文件',
            b'\xff\xfb': 'MP3文件',
            b'\x49\x44\x33': 'MP3 ID3标签',
            b'\x1a\x45\xdf\xa3': 'WebM/Matroska',
            b'\x00\x00\x00': '可能为其他格式'
        }
        
        for sig, desc in audio_signatures.items():
            if header.startswith(sig):
                print(f"检测到: {desc}")
                break
        else:
            print("未知音频格式")
            
else:
    print("❌ 音频文件不存在")
    # 创建测试文件
    print("创建测试音频文件...")
    test_dir = tempfile.gettempdir()
    test_audio_path = os.path.join(test_dir, "test_voice.wav")
    
    # 创建一个简单的WAV文件头
    import struct
    sample_rate = 16000
    duration = 2  # 2秒
    num_samples = sample_rate * duration
    
    with open(test_audio_path, 'wb') as f:
        # WAV文件头
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + num_samples * 2))  # 文件大小
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))  # PCM格式块大小
        f.write(struct.pack('<H', 1))   # 音频格式：PCM
        f.write(struct.pack('<H', 1))   # 声道数：单声道
        f.write(struct.pack('<I', sample_rate))  # 采样率
        f.write(struct.pack('<I', sample_rate * 2))  # 字节率
        f.write(struct.pack('<H', 2))   # 块对齐
        f.write(struct.pack('<H', 16))  # 位深度
        f.write(b'data')
        f.write(struct.pack('<I', num_samples * 2))  # 数据大小
        
        # 生成简单的正弦波
        import math
        frequency = 440  # A4音
        for i in range(num_samples):
            sample = int(32767 * math.sin(2 * math.pi * frequency * i / sample_rate))
            f.write(struct.pack('<h', sample))
    
    print(f"创建测试文件: {test_audio_path}")

print("\n=== 语音识别方案测试 ===")

# 方案1: 尝试使用Whisper
print("\n1. 测试Whisper语音识别...")
try:
    import whisper
    print("✅ Whisper库导入成功")
    
    # 检查模型
    print("可用模型: tiny, base, small, medium, large")
    print("推荐: 'base' 模型（平衡速度和准确率）")
    
    # 注意：首次运行会下载模型
    print("首次运行需要下载模型，请耐心等待...")
    
except ImportError:
    print("❌ Whisper库未安装")
    print("安装命令: pip install openai-whisper")
    print("正在安装中...")

# 方案2: Windows语音识别
print("\n2. 测试Windows语音识别...")
try:
    import win32com.client
    print("✅ win32com导入成功")
    
    # 测试语音合成
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    print("Windows语音合成可用")
    
    # 尝试语音识别（需要配置）
    try:
        recognizer = win32com.client.Dispatch("SAPI.SpSharedRecognizer")
        print("Windows语音识别可用")
    except:
        print("Windows语音识别需要配置")
        
except ImportError:
    print("❌ win32com未安装")
    print("安装命令: pip install pywin32")

# 方案3: 音频处理库
print("\n3. 测试音频处理库...")
try:
    import wave
    print("✅ wave库可用 - 支持WAV文件")
except:
    print("wave库不可用")

try:
    import pydub
    print("✅ pydub库可用 - 支持多种音频格式")
except:
    print("pydub库未安装")
    print("安装命令: pip install pydub")

print("\n=== 实施建议 ===")
print("1. 优先完成Whisper安装")
print("2. 测试Whisper识别准确率")
print("3. 集成到QQ语音处理流程")
print("4. 对比平台ASR和Whisper结果")

print("\n语音识别优化测试完成")