#!/usr/bin/env python3
# 音频预处理提升识别准确率
import os
import tempfile
import sys

def preprocess_audio(input_path, output_path=None):
    """
    音频预处理：音量标准化 + 简单降噪
    """
    print(f"音频预处理: {input_path}")
    
    if not os.path.exists(input_path):
        print("输入文件不存在")
        return None
    
    if output_path is None:
        temp_dir = tempfile.gettempdir()
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(temp_dir, f"preprocessed_{name}.wav")
    
    try:
        # 尝试使用pydub进行音频处理
        try:
            from pydub import AudioSegment
            from pydub.effects import normalize
            
            print("使用pydub进行音频预处理...")
            
            # 加载音频
            audio = AudioSegment.from_file(input_path)
            
            print(f"原始音频信息:")
            print(f"  时长: {len(audio)/1000:.1f}秒")
            print(f"  采样率: {audio.frame_rate}Hz")
            print(f"  声道数: {audio.channels}")
            print(f"  位深度: {audio.sample_width * 8}位")
            
            # 1. 转换为单声道（提高识别准确率）
            if audio.channels > 1:
                print("转换为单声道...")
                audio = audio.set_channels(1)
            
            # 2. 标准化音量
            print("标准化音量...")
            audio = normalize(audio)
            
            # 3. 调整采样率（Whisper推荐16kHz）
            target_rate = 16000
            if audio.frame_rate != target_rate:
                print(f"调整采样率: {audio.frame_rate}Hz -> {target_rate}Hz")
                audio = audio.set_frame_rate(target_rate)
            
            # 4. 简单降噪（通过高通滤波）
            print("应用简单降噪...")
            # 移除低频噪音（50Hz以下）
            audio = audio.high_pass_filter(50)
            
            # 5. 保存预处理后的音频
            print(f"保存预处理音频: {output_path}")
            audio.export(output_path, format="wav")
            
            # 验证输出
            processed = AudioSegment.from_file(output_path)
            print(f"\n预处理后音频信息:")
            print(f"  时长: {len(processed)/1000:.1f}秒")
            print(f"  采样率: {processed.frame_rate}Hz")
            print(f"  声道数: {processed.channels}")
            print(f"  文件大小: {os.path.getsize(output_path)}字节")
            
            return output_path
            
        except ImportError:
            print("pydub未安装，使用简单预处理")
            print("安装命令: pip install pydub")
            
            # 简单复制
            import shutil
            shutil.copy2(input_path, output_path)
            print(f"简单复制到: {output_path}")
            return output_path
            
    except Exception as e:
        print(f"预处理错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_preprocessing_effect(audio_path):
    """
    测试预处理效果
    """
    print("\n=== 音频预处理效果测试 ===")
    
    # 预处理音频
    preprocessed = preprocess_audio(audio_path)
    if not preprocessed:
        return
    
    # 使用Whisper测试预处理效果
    try:
        import whisper
        
        print("\n测试预处理前后识别效果...")
        
        # 加载base模型
        model = whisper.load_model("base")
        
        # 测试原始音频
        print("\n1. 原始音频识别:")
        result_raw = model.transcribe(audio_path, language="zh", temperature=0.2)
        print(f"   识别结果: {result_raw['text'].strip()}")
        
        # 测试预处理音频
        print("\n2. 预处理后音频识别:")
        result_processed = model.transcribe(preprocessed, language="zh", temperature=0.2)
        print(f"   识别结果: {result_processed['text'].strip()}")
        
        # 对比分析
        print("\n=== 预处理效果分析 ===")
        raw_text = result_raw['text'].strip()
        proc_text = result_processed['text'].strip()
        
        if raw_text == proc_text:
            print("识别结果相同，预处理效果不明显")
        else:
            print("识别结果不同，预处理可能影响识别")
            
            # 简单相似度计算
            if raw_text and proc_text:
                matches = sum(1 for a, b in zip(raw_text, proc_text) if a == b)
                similarity = matches / max(len(raw_text), len(proc_text)) * 100
                print(f"文本相似度: {similarity:.1f}%")
        
        # 保存测试报告
        import tempfile
        temp_dir = tempfile.gettempdir()
        report_file = os.path.join(temp_dir, "preprocessing_test_report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=== 音频预处理效果测试报告 ===\n\n")
            f.write(f"原始音频: {audio_path}\n")
            f.write(f"预处理音频: {preprocessed}\n\n")
            f.write("=== 识别结果对比 ===\n")
            f.write(f"原始音频识别: {raw_text}\n")
            f.write(f"预处理后识别: {proc_text}\n\n")
            f.write("=== 预处理步骤 ===\n")
            f.write("1. 转换为单声道\n")
            f.write("2. 音量标准化\n")
            f.write("3. 采样率调整到16kHz\n")
            f.write("4. 高通滤波降噪(50Hz)\n")
        
        print(f"\n测试报告: {report_file}")
        print(f"预处理音频: {preprocessed}")
        
    except ImportError:
        print("Whisper未安装")

if __name__ == "__main__":
    # 测试最新的音频文件
    test_audio = r"C:\Users\Administrator\.openclaw\qqbot\downloads\fca6ab22012bea2e558b4208f531f935.bin"
    
    if os.path.exists(test_audio):
        test_preprocessing_effect(test_audio)
    else:
        print(f"测试音频不存在: {test_audio}")
        
        # 创建测试文件
        print("创建测试音频...")
        import wave
        import struct
        import math
        
        temp_dir = tempfile.gettempdir()
        test_file = os.path.join(temp_dir, "test_audio_preprocess.wav")
        
        sample_rate = 16000
        duration = 2
        
        with wave.open(test_file, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            
            for i in range(sample_rate * duration):
                value = int(32767 * 0.5 * math.sin(2 * math.pi * 440 * i / sample_rate))
                wav.writeframes(struct.pack('<h', value))
        
        print(f"创建测试文件: {test_file}")
        test_preprocessing_effect(test_file)