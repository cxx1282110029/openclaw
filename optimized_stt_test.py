#!/usr/bin/env python3
# 优化后的语音识别测试
import os
import tempfile
import sys

def run_optimized_test():
    print("=== 语音识别优化测试 ===")
    
    # 设置UTF-8编码
    sys.stdout.reconfigure(encoding='utf-8')
    
    # 新语音文件
    new_audio = r"C:\Users\Administrator\.openclaw\qqbot\downloads\6b33377d950153a881b3b5f9f649fc5b.bin"
    qq_asr_text = "喂喂喂，你好你好你好。"
    
    print(f"测试音频: {new_audio}")
    print(f"QQ平台ASR: {qq_asr_text}")
    
    if os.path.exists(new_audio):
        file_size = os.path.getsize(new_audio)
        print(f"音频文件大小: {file_size} 字节")
        
        # 使用Whisper base模型识别
        try:
            import whisper
            
            print("\n1. 使用Whisper base模型识别...")
            model = whisper.load_model("base")
            
            # 识别
            result = model.transcribe(new_audio, language="zh", task="transcribe")
            
            print("\n=== Whisper识别结果 ===")
            whisper_text = result['text'].strip()
            print(f"识别文本: {whisper_text}")
            print(f"识别语言: {result['language']}")
            
            # 详细分析
            print("\n=== 识别质量分析 ===")
            
            # 1. 文本长度对比
            qq_len = len(qq_asr_text)
            whisper_len = len(whisper_text)
            print(f"文本长度 - QQ ASR: {qq_len}字符, Whisper: {whisper_len}字符")
            
            # 2. 相似度分析（简单版）
            similarity = 0
            if whisper_text and qq_asr_text:
                # 简单字符匹配
                matches = sum(1 for a, b in zip(whisper_text, qq_asr_text) if a == b)
                similarity = matches / max(len(whisper_text), len(qq_asr_text)) * 100
                print(f"文本相似度: {similarity:.1f}%")
            
            # 3. 唤醒词检测
            print("\n=== 唤醒词检测 ===")
            wake_words = ["龙虾", "openclaw", "贾维斯"]
            text_lower = whisper_text.lower()
            
            detected = []
            for word in wake_words:
                if word.lower() in text_lower:
                    detected.append(word)
                    print(f"检测到唤醒词: {word}")
                else:
                    print(f"未检测到: {word}")
            
            # 4. 生成语音响应
            print("\n=== 生成语音响应 ===")
            if detected:
                response_text = f"检测到唤醒词{detected[0]}，语音识别优化测试成功！"
            else:
                response_text = f"收到消息：{whisper_text[:20]}...，语音识别准确率优化测试中"
            
            print(f"响应文本: {response_text}")
            
            # 生成语音文件
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 0.9)
            
            temp_dir = tempfile.gettempdir()
            response_file = os.path.join(temp_dir, "optimized_response.mp3")
            
            engine.save_to_file(response_text, response_file)
            engine.runAndWait()
            
            if os.path.exists(response_file):
                resp_size = os.path.getsize(response_file)
                print(f"语音响应生成成功: {response_file} ({resp_size} 字节)")
                
                # 保存测试报告
                report_file = os.path.join(temp_dir, "stt_optimization_report.txt")
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write("=== 语音识别优化测试报告 ===\n\n")
                    f.write(f"测试时间: 2026-03-21 10:54\n")
                    f.write(f"音频文件: {new_audio}\n")
                    f.write(f"文件大小: {file_size} 字节\n\n")
                    f.write("=== 识别结果对比 ===\n")
                    f.write(f"QQ平台ASR: {qq_asr_text}\n")
                    f.write(f"Whisper识别: {whisper_text}\n")
                    f.write(f"识别语言: {result['language']}\n")
                    f.write(f"文本相似度: {similarity:.1f}%\n\n")
                    f.write("=== 唤醒词检测 ===\n")
                    for word in wake_words:
                        status = "检测到" if word.lower() in text_lower else "未检测到"
                        f.write(f"{word}: {status}\n")
                    f.write(f"\n检测到的唤醒词: {detected}\n\n")
                    f.write("=== 优化效果评估 ===\n")
                    if similarity > 80:
                        f.write("优化效果显著：识别准确率高\n")
                    elif similarity > 60:
                        f.write("优化效果一般：识别准确率中等\n")
                    else:
                        f.write("需要进一步优化：识别准确率低\n")
                    f.write(f"\n语音响应文件: {response_file}\n")
                
                print(f"\n测试报告已保存: {report_file}")
                print(f"语音响应文件: {response_file}")
                
                return response_file
                
            else:
                print("语音响应生成失败")
                return None
                
        except ImportError:
            print("Whisper未安装")
            return None
        except Exception as e:
            print(f"识别错误: {e}")
            import traceback
            traceback.print_exc()
            return None
            
    else:
        print("音频文件不存在")
        return None

if __name__ == "__main__":
    result = run_optimized_test()
    if result:
        print(f"\n语音识别优化测试完成，响应文件: {result}")
    else:
        print("\n语音识别优化测试失败")