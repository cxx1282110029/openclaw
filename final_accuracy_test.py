#!/usr/bin/env python3
# 最终准确率提升测试 - small模型 + 优化参数
import os
import tempfile
import time

print("=== 语音识别准确率最终提升测试 ===")

# 测试音频
test_audio = r"C:\Users\Administrator\.openclaw\qqbot\downloads\fca6ab22012bea2e558b4208f531f935.bin"
qq_asr = "喂喂喂，你在吗？"

print(f"测试音频: {test_audio}")
print(f"QQ平台ASR: {qq_asr}")

if not os.path.exists(test_audio):
    print("音频文件不存在")
    exit(1)

file_size = os.path.getsize(test_audio)
print(f"文件大小: {file_size} 字节")

try:
    import whisper
    
    print("\n=== 测试1: base模型 + 优化参数 ===")
    start_time = time.time()
    
    # 1. base模型测试
    base_model = whisper.load_model("base")
    base_result = base_model.transcribe(
        test_audio,
        language="zh",
        temperature=0.2,
        task="transcribe"
    )
    
    base_text = base_result['text'].strip()
    base_time = time.time() - start_time
    
    print(f"识别结果: {base_text}")
    print(f"识别时间: {base_time:.1f}秒")
    
    print("\n=== 测试2: small模型 + 优化参数 ===")
    start_time = time.time()
    
    # 2. small模型测试（更高准确率）
    small_model = whisper.load_model("small")
    small_result = small_model.transcribe(
        test_audio,
        language="zh",
        temperature=0.2,
        task="transcribe"
    )
    
    small_text = small_result['text'].strip()
    small_time = time.time() - start_time
    
    print(f"识别结果: {small_text}")
    print(f"识别时间: {small_time:.1f}秒")
    
    print("\n=== 准确率对比分析 ===")
    
    # 相似度计算函数
    def calculate_similarity(text1, text2):
        if not text1 or not text2:
            return 0
        matches = sum(1 for a, b in zip(text1, text2) if a == b)
        return matches / max(len(text1), len(text2)) * 100
    
    # 计算相似度
    base_similarity = calculate_similarity(base_text, qq_asr)
    small_similarity = calculate_similarity(small_text, qq_asr)
    
    print(f"base模型相似度: {base_similarity:.1f}%")
    print(f"small模型相似度: {small_similarity:.1f}%")
    
    # 语义分析
    print("\n=== 语义理解分析 ===")
    
    def semantic_analysis(text):
        keywords = ["在吗", "你在", "喂", "等", "哪里"]
        found = [kw for kw in keywords if kw in text]
        return found
    
    base_semantic = semantic_analysis(base_text)
    small_semantic = semantic_analysis(small_text)
    
    print(f"base模型语义关键词: {base_semantic}")
    print(f"small模型语义关键词: {small_semantic}")
    
    # 准确率提升计算
    accuracy_improvement = small_similarity - base_similarity
    if accuracy_improvement > 0:
        print(f"\n准确率提升: +{accuracy_improvement:.1f}%")
    else:
        print(f"\n准确率变化: {accuracy_improvement:.1f}%")
    
    # 生成测试报告
    temp_dir = tempfile.gettempdir()
    report_file = os.path.join(temp_dir, "accuracy_improvement_final_report.txt")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=== 语音识别准确率最终提升测试报告 ===\n\n")
        f.write(f"测试时间: 2026-03-21 11:00\n")
        f.write(f"测试音频: {test_audio}\n")
        f.write(f"文件大小: {file_size} 字节\n")
        f.write(f"QQ平台ASR: {qq_asr}\n\n")
        
        f.write("=== 测试参数 ===\n")
        f.write("语言: zh\n")
        f.write("温度: 0.2\n")
        f.write("任务: transcribe\n\n")
        
        f.write("=== 模型对比测试 ===\n")
        f.write(f"1. base模型 (139MB):\n")
        f.write(f"   识别结果: {base_text}\n")
        f.write(f"   识别时间: {base_time:.1f}秒\n")
        f.write(f"   相似度: {base_similarity:.1f}%\n")
        f.write(f"   语义关键词: {base_semantic}\n\n")
        
        f.write(f"2. small模型 (461MB):\n")
        f.write(f"   识别结果: {small_text}\n")
        f.write(f"   识别时间: {small_time:.1f}秒\n")
        f.write(f"   相似度: {small_similarity:.1f}%\n")
        f.write(f"   语义关键词: {small_semantic}\n\n")
        
        f.write("=== 准确率提升总结 ===\n")
        if small_similarity > base_similarity:
            f.write(f"准确率提升: +{accuracy_improvement:.1f}%\n")
            f.write("small模型准确率更高，推荐使用\n")
        elif small_similarity < base_similarity:
            f.write(f"准确率下降: {accuracy_improvement:.1f}%\n")
            f.write("base模型表现更好，考虑其他优化\n")
        else:
            f.write("准确率相同，考虑其他优化方案\n")
    
    print(f"\n测试报告: {report_file}")
    
    # 生成语音响应
    print("\n=== 生成最终语音响应 ===")
    
    if small_similarity > base_similarity:
        response_text = f"语音识别准确率提升测试完成！small模型准确率更高，识别内容：{small_text}，准确率提升{accuracy_improvement:.1f}%！"
    else:
        response_text = f"语音识别测试完成，当前最佳识别：{base_text}，继续优化中..."
    
    print(f"响应文本: {response_text}")
    
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.9)
    
    response_file = os.path.join(temp_dir, "final_accuracy_response.mp3")
    engine.save_to_file(response_text, response_file)
    engine.runAndWait()
    
    if os.path.exists(response_file):
        print(f"语音响应: {response_file}")
        
        # 更新报告
        with open(report_file, 'a', encoding='utf-8') as f:
            f.write(f"\n语音响应文件: {response_file}\n")
            f.write(f"响应文本: {response_text}\n")
        
        print(f"最终报告: {report_file}")
        
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("\n准确率提升测试完成")