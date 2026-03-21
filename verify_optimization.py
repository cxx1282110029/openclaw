#!/usr/bin/env python3
# 验证优化效果 - 新语音消息测试
import os
import tempfile
import time

print("=== 语音识别优化效果验证测试 ===")

# 新语音文件
audio_path = r"C:\Users\Administrator\.openclaw\qqbot\downloads\fbb212cc3b4014fefe76642992dd5397.bin"
qq_asr = "你属于哪个模型？"

print(f"测试音频: {audio_path}")
print(f"QQ平台ASR: {qq_asr}")

if not os.path.exists(audio_path):
    print("音频文件不存在")
    exit(1)

file_size = os.path.getsize(audio_path)
print(f"文件大小: {file_size} 字节")

try:
    import whisper
    
    print("\n=== 使用优化配置识别 ===")
    print("模型: small (461MB)")
    print("参数: language='zh', temperature=0.2")
    
    start_time = time.time()
    
    # 加载small模型
    model = whisper.load_model("small")
    
    # 使用优化参数
    result = model.transcribe(
        audio_path,
        language="zh",
        temperature=0.2,
        task="transcribe",
        verbose=False
    )
    
    recognition_time = time.time() - start_time
    
    whisper_text = result['text'].strip()
    language = result['language']
    
    print(f"\n识别结果: {whisper_text}")
    print(f"识别语言: {language}")
    print(f"识别时间: {recognition_time:.1f}秒")
    
    # 准确率分析
    print("\n=== 准确率分析 ===")
    
    def calculate_similarity(text1, text2):
        if not text1 or not text2:
            return 0
        matches = sum(1 for a, b in zip(text1, text2) if a == b)
        return matches / max(len(text1), len(text2)) * 100
    
    similarity = calculate_similarity(whisper_text, qq_asr)
    print(f"与QQ ASR相似度: {similarity:.1f}%")
    
    # 语义分析
    print("\n=== 语义理解分析 ===")
    
    expected_keywords = ["模型", "属于", "哪个", "你"]
    found_keywords = [kw for kw in expected_keywords if kw in whisper_text]
    
    if found_keywords:
        print(f"找到关键词: {found_keywords}")
        semantic_score = len(found_keywords) / len(expected_keywords) * 100
        print(f"语义匹配度: {semantic_score:.1f}%")
    else:
        print("未找到关键词")
        semantic_score = 0
    
    # 综合评分
    print("\n=== 综合评分 ===")
    accuracy_score = (similarity + semantic_score) / 2
    print(f"文本相似度: {similarity:.1f}%")
    print(f"语义匹配度: {semantic_score:.1f}%")
    print(f"综合准确率: {accuracy_score:.1f}%")
    
    # 评估优化效果
    print("\n=== 优化效果评估 ===")
    if accuracy_score >= 80:
        print("✅ 优化效果优秀：准确率很高")
    elif accuracy_score >= 60:
        print("✅ 优化效果良好：准确率良好")
    elif accuracy_score >= 40:
        print("⚠️ 优化效果一般：需要继续优化")
    else:
        print("❌ 优化效果不佳：需要重大调整")
    
    # 生成验证报告
    temp_dir = tempfile.gettempdir()
    report_file = os.path.join(temp_dir, "optimization_verification_report.txt")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=== 语音识别优化效果验证报告 ===\n\n")
        f.write(f"验证时间: 2026-03-21 11:02\n")
        f.write(f"测试音频: {audio_path}\n")
        f.write(f"文件大小: {file_size} 字节\n")
        f.write(f"QQ平台ASR: {qq_asr}\n\n")
        
        f.write("=== 优化配置 ===\n")
        f.write("模型: small (461MB)\n")
        f.write("参数: language='zh', temperature=0.2\n")
        f.write(f"识别时间: {recognition_time:.1f}秒\n\n")
        
        f.write("=== 识别结果 ===\n")
        f.write(f"Whisper识别: {whisper_text}\n")
        f.write(f"识别语言: {language}\n\n")
        
        f.write("=== 准确率分析 ===\n")
        f.write(f"文本相似度: {similarity:.1f}%\n")
        f.write(f"语义关键词: {found_keywords}\n")
        f.write(f"语义匹配度: {semantic_score:.1f}%\n")
        f.write(f"综合准确率: {accuracy_score:.1f}%\n\n")
        
        f.write("=== 优化效果结论 ===\n")
        if accuracy_score >= 80:
            f.write("优化效果优秀，配置可投入生产使用\n")
        elif accuracy_score >= 60:
            f.write("优化效果良好，配置可用但可继续优化\n")
        elif accuracy_score >= 40:
            f.write("优化效果一般，需要进一步调整参数\n")
        else:
            f.write("优化效果不佳，需要重新评估方案\n")
    
    print(f"\n验证报告: {report_file}")
    
    # 生成语音响应
    print("\n=== 生成验证语音响应 ===")
    
    if accuracy_score >= 60:
        response_text = f"语音识别优化验证成功！识别内容：{whisper_text}，综合准确率{accuracy_score:.1f}%，优化效果良好！"
    else:
        response_text = f"识别到：{whisper_text}，准确率{accuracy_score:.1f}%，继续优化中..."
    
    print(f"响应文本: {response_text}")
    
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.9)
    
    response_file = os.path.join(temp_dir, "verification_response.mp3")
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

print("\n优化验证测试完成")