#!/usr/bin/env python3
# 实时语音识别速度测试
import os
import tempfile
import time

print("=== 实时语音识别速度测试 ===")

# 新语音文件
audio_path = r"C:\Users\Administrator\.openclaw\qqbot\downloads\b2eaa2fca99b338fe5ee8bc803a5317d.bin"
qq_asr = "你是哪个模型？"

print(f"测试音频: {audio_path}")
print(f"QQ平台ASR: {qq_asr}")

if not os.path.exists(audio_path):
    print("音频文件不存在")
    exit(1)

file_size = os.path.getsize(audio_path)
print(f"文件大小: {file_size} 字节")

try:
    import whisper
    
    print("\n=== 测试1: tiny模型实时识别 ===")
    print("配置: 预加载 + temperature=0.2")
    
    # 预加载tiny模型（最快）
    start_load = time.time()
    model = whisper.load_model("tiny")
    load_time = time.time() - start_load
    
    print(f"模型加载时间: {load_time:.2f}秒")
    
    # 实时识别测试
    print("\n开始实时识别...")
    
    start_recognition = time.time()
    result = model.transcribe(
        audio_path,
        language="zh",
        temperature=0.2,
        task="transcribe",
        verbose=False
    )
    
    recognition_time = time.time() - start_recognition
    total_time = time.time() - start_load
    
    whisper_text = result['text'].strip()
    
    print(f"\n识别结果: {whisper_text}")
    print(f"识别语言: {result['language']}")
    print(f"识别时间: {recognition_time:.2f}秒")
    print(f"总时间(含加载): {total_time:.2f}秒")
    
    # 准确率分析
    print("\n=== 准确率分析 ===")
    
    def calculate_similarity(text1, text2):
        if not text1 or not text2:
            return 0
        matches = sum(1 for a, b in zip(text1, text2) if a == b)
        return matches / max(len(text1), len(text2)) * 100
    
    similarity = calculate_similarity(whisper_text, qq_asr)
    print(f"文本相似度: {similarity:.1f}%")
    
    # 语义分析
    expected_keywords = ["模型", "哪个", "你", "是"]
    found_keywords = [kw for kw in expected_keywords if kw in whisper_text]
    
    if found_keywords:
        semantic_score = len(found_keywords) / len(expected_keywords) * 100
        print(f"语义关键词: {found_keywords}")
        print(f"语义匹配度: {semantic_score:.1f}%")
    else:
        semantic_score = 0
        print("未找到语义关键词")
    
    # 综合评分
    accuracy_score = (similarity + semantic_score) / 2
    print(f"综合准确率: {accuracy_score:.1f}%")
    
    # 速度评级
    print("\n=== 速度评级 ===")
    if recognition_time < 0.3:
        speed_rating = "⚡ 极速 (实时响应)"
    elif recognition_time < 0.5:
        speed_rating = "🚀 快速 (良好体验)"
    elif recognition_time < 1.0:
        speed_rating = "🐇 中等 (可接受)"
    else:
        speed_rating = "🐢 较慢 (需优化)"
    
    print(f"识别速度: {recognition_time:.2f}秒 - {speed_rating}")
    
    # 与优化前对比
    print("\n=== 优化前后对比 ===")
    print(f"优化前(small模型): 3.0秒")
    print(f"优化后(tiny模型): {recognition_time:.2f}秒")
    
    if recognition_time > 0:
        speed_improvement = 3.0 / recognition_time
        print(f"速度提升: {speed_improvement:.1f}倍")
    
    # 生成测试报告
    temp_dir = tempfile.gettempdir()
    report_file = os.path.join(temp_dir, "real_time_speed_report.txt")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=== 实时语音识别速度测试报告 ===\n\n")
        f.write(f"测试时间: 2026-03-21 11:05\n")
        f.write(f"测试音频: {audio_path}\n")
        f.write(f"文件大小: {file_size} 字节\n")
        f.write(f"QQ平台ASR: {qq_asr}\n\n")
        
        f.write("=== 优化配置 ===\n")
        f.write("模型: tiny (72MB)\n")
        f.write("参数: language='zh', temperature=0.2\n")
        f.write(f"模型加载: {load_time:.2f}秒\n")
        f.write(f"识别时间: {recognition_time:.2f}秒\n")
        f.write(f"总时间: {total_time:.2f}秒\n\n")
        
        f.write("=== 识别结果 ===\n")
        f.write(f"Whisper识别: {whisper_text}\n")
        f.write(f"识别语言: {result['language']}\n\n")
        
        f.write("=== 准确率分析 ===\n")
        f.write(f"文本相似度: {similarity:.1f}%\n")
        f.write(f"语义关键词: {found_keywords}\n")
        f.write(f"语义匹配度: {semantic_score:.1f}%\n")
        f.write(f"综合准确率: {accuracy_score:.1f}%\n\n")
        
        f.write("=== 速度评估 ===\n")
        f.write(f"识别速度: {recognition_time:.2f}秒 - {speed_rating}\n")
        f.write(f"优化前对比: 3.0秒 → {recognition_time:.2f}秒\n")
        if recognition_time > 0:
            f.write(f"速度提升: {3.0/recognition_time:.1f}倍\n")
        
        f.write("\n=== 优化效果结论 ===\n")
        if recognition_time < 0.5 and accuracy_score > 60:
            f.write("✅ 优化效果优秀：实时响应 + 高准确率\n")
        elif recognition_time < 1.0 and accuracy_score > 40:
            f.write("✅ 优化效果良好：快速响应 + 可接受准确率\n")
        else:
            f.write("⚠️ 优化效果一般：需要进一步调整\n")
    
    print(f"\n测试报告: {report_file}")
    
    # 生成实时语音响应
    print("\n=== 生成实时语音响应 ===")
    
    if recognition_time < 0.5:
        response_text = f"实时语音识别成功！仅需{recognition_time:.2f}秒，识别内容：{whisper_text}，速度提升明显！"
    else:
        response_text = f"识别到：{whisper_text}，识别时间{recognition_time:.2f}秒，继续优化中..."
    
    print(f"响应文本: {response_text}")
    
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.9)
    
    response_file = os.path.join(temp_dir, "real_time_response.mp3")
    engine.save_to_file(response_text, response_file)
    engine.runAndWait()
    
    if os.path.exists(response_file):
        print(f"语音响应: {response_file}")
        
        # 更新报告
        with open(report_file, 'a', encoding='utf-8') as f:
            f.write(f"\n语音响应文件: {response_file}\n")
            f.write(f"响应文本: {response_text}\n")
        
        print(f"最终报告: {report_file}")
        
        return response_file
        
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("\n实时速度测试完成")