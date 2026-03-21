#!/usr/bin/env python3
# QQ音频文件转换工具
import os
import tempfile
import shutil

def convert_qq_audio(input_path, output_format="wav"):
    """
    转换QQ音频文件为标准格式
    """
    print(f"转换QQ音频文件: {input_path} -> {output_format}")
    
    if not os.path.exists(input_path):
        print("输入文件不存在")
        return None
    
    # 获取文件信息
    file_size = os.path.getsize(input_path)
    print(f"原始文件大小: {file_size} 字节")
    
    # 读取文件头判断格式
    with open(input_path, 'rb') as f:
        header = f.read(100)  # 读取前100字节
        
    print(f"文件头(hex): {header[:20].hex()}")
    
    # 常见音频格式检测
    if header.startswith(b'RIFF'):
        print("检测到: WAV格式")
        ext = "wav"
    elif header.startswith(b'\xff\xfb') or header.startswith(b'\x49\x44\x33'):
        print("检测到: MP3格式")
        ext = "mp3"
    elif header.startswith(b'\x1a\x45\xdf\xa3'):
        print("检测到: WebM/Matroska格式")
        ext = "webm"
    elif header.startswith(b'fLaC'):
        print("检测到: FLAC格式")
        ext = "flac"
    else:
        print("未知格式，尝试作为原始音频处理")
        ext = "bin"
    
    # 创建输出文件
    temp_dir = tempfile.gettempdir()
    output_file = os.path.join(temp_dir, f"converted_audio.{output_format}")
    
    try:
        # 简单复制（如果已经是目标格式）
        if ext == output_format:
            print("文件已经是目标格式，直接复制")
            shutil.copy2(input_path, output_file)
        else:
            print(f"需要格式转换: {ext} -> {output_format}")
            
            # 尝试使用pydub转换
            try:
                from pydub import AudioSegment
                
                # 根据扩展名加载
                if ext == "wav":
                    audio = AudioSegment.from_wav(input_path)
                elif ext == "mp3":
                    audio = AudioSegment.from_mp3(input_path)
                elif ext == "webm":
                    audio = AudioSegment.from_file(input_path, format="webm")
                else:
                    # 尝试自动检测
                    audio = AudioSegment.from_file(input_path)
                
                # 转换为目标格式
                if output_format == "wav":
                    audio.export(output_file, format="wav")
                elif output_format == "mp3":
                    audio.export(output_file, format="mp3", bitrate="128k")
                else:
                    audio.export(output_file, format=output_format)
                
                print(f"转换成功: {output_file}")
                
            except ImportError:
                print("pydub未安装，使用简单复制")
                print("安装命令: pip install pydub")
                shutil.copy2(input_path, output_file)
                
            except Exception as e:
                print(f"pydub转换失败: {e}")
                print("使用简单复制")
                shutil.copy2(input_path, output_file)
        
        # 验证输出文件
        if os.path.exists(output_file):
            out_size = os.path.getsize(output_file)
            print(f"输出文件大小: {out_size} 字节")
            return output_file
        else:
            print("输出文件创建失败")
            return None
            
    except Exception as e:
        print(f"转换错误: {e}")
        return None

def test_whisper_with_converted(audio_path):
    """
    使用转换后的音频测试Whisper
    """
    print("\n=== 使用转换音频测试Whisper ===")
    
    try:
        import whisper
        
        # 转换音频为WAV格式
        wav_file = convert_qq_audio(audio_path, "wav")
        if not wav_file:
            print("音频转换失败")
            return
        
        print(f"使用音频文件: {wav_file}")
        
        # 加载更大的模型提高准确率
        print("加载Whisper base模型...")
        model = whisper.load_model("base")  # 比tiny更准确
        
        # 识别
        print("开始识别...")
        result = model.transcribe(wav_file, language="zh", task="transcribe")
        
        print("\n=== 识别结果 ===")
        print(f"文本: {result['text']}")
        print(f"语言: {result['language']}")
        print(f"置信度: {result.get('confidence', 'N/A')}")
        
        # 详细分析
        if 'segments' in result:
            print("\n=== 分段详情 ===")
            for i, segment in enumerate(result['segments'][:3]):  # 只显示前3段
                print(f"段 {i+1}: {segment['text']} (开始: {segment['start']:.1f}s, 结束: {segment['end']:.1f}s)")
        
        # 保存详细结果
        result_file = os.path.join(tempfile.gettempdir(), "whisper_detailed.txt")
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"音频文件: {audio_path}\n")
            f.write(f"转换文件: {wav_file}\n")
            f.write(f"模型: base\n")
            f.write(f"识别文本: {result['text']}\n")
            f.write(f"语言: {result['language']}\n")
            f.write(f"QQ平台ASR: 喂，龙虾你好。\n")
            
            if 'segments' in result:
                f.write("\n分段详情:\n")
                for seg in result['segments']:
                    f.write(f"  [{seg['start']:.1f}s - {seg['end']:.1f}s]: {seg['text']}\n")
        
        print(f"\n详细结果已保存: {result_file}")
        
    except ImportError:
        print("Whisper未安装")
    except Exception as e:
        print(f"Whisper测试错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 测试QQ音频文件
    qq_audio = r"C:\Users\Administrator\.openclaw\qqbot\downloads\65b66a8277dce336fd2792cf660d9c2d.bin"
    
    if os.path.exists(qq_audio):
        test_whisper_with_converted(qq_audio)
    else:
        print(f"QQ音频文件不存在: {qq_audio}")
        
        # 创建测试文件
        print("创建测试音频...")
        import wave
        import struct
        import math
        
        temp_dir = tempfile.gettempdir()
        test_file = os.path.join(temp_dir, "test_chinese_voice.wav")
        
        sample_rate = 16000
        duration = 3
        
        with wave.open(test_file, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            
            # 生成包含"龙虾你好"频率模式的测试音频
            for i in range(sample_rate * duration):
                # 简单的测试信号
                value = int(32767 * 0.3 * math.sin(2 * math.pi * 440 * i / sample_rate))
                wav.writeframes(struct.pack('<h', value))
        
        print(f"创建测试文件: {test_file}")
        test_whisper_with_converted(test_file)