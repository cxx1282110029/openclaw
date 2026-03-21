#!/usr/bin/env python3
import os, tempfile, time

audio_path = r"C:\Users\Administrator\.openclaw\qqbot\downloads\b2eaa2fca99b338fe5ee8bc803a5317d.bin"
qq_asr = "你是哪个模型？"

print("=== 实时语音识别速度测试 ===")
print(f"音频: {audio_path}")
print(f"QQ ASR: {qq_asr}")

if os.path.exists(audio_path):
    import whisper
    
    # 预加载tiny模型
    print("\n预加载tiny模型...")
    start_load = time.time()
    model = whisper.load_model("tiny")
    load_time = time.time() - start_load
    
    print(f"模型加载: {load_time:.2f}秒")
    
    # 实时识别
    print("\n开始实时识别...")
    start_recog = time.time()
    
    result = model.transcribe(audio_path, language="zh", temperature=0.2)
    recog_time = time.time() - start_recog
    
    text = result['text'].strip()
    total_time = time.time() - start_load
    
    print(f"\n识别结果: {text}")
    print(f"识别语言: {result['language']}")
    print(f"识别时间: {recog_time:.2f}秒")
    print(f"总时间: {total_time:.2f}秒")
    
    # 相似度
    matches = sum(1 for a, b in zip(text, qq_asr) if a == b)
    similarity = matches / max(len(text), len(qq_asr)) * 100
    print(f"相似度: {similarity:.1f}%")
    
    # 速度评级
    if recog_time < 0.3:
        rating = "⚡ 极速 (实时响应)"
    elif recog_time < 0.5:
        rating = "🚀 快速 (良好体验)"
    elif recog_time < 1.0:
        rating = "🐇 中等 (可接受)"
    else:
        rating = "🐢 较慢 (需优化)"
    
    print(f"速度评级: {rating}")
    
    # 优化对比
    print(f"\n优化对比:")
    print(f"优化前(small): 3.0秒")
    print(f"优化后(tiny): {recog_time:.2f}秒")
    
    if recog_time > 0:
        improvement = 3.0 / recog_time
        print(f"速度提升: {improvement:.1f}倍")
    
    # 生成响应
    import pyttsx3
    engine = pyttsx3.init()
    
    if recog_time < 0.5:
        response = f"实时语音识别成功！仅需{recog_time:.2f}秒，识别内容：{text}，速度提升{improvement:.1f}倍！"
    else:
        response = f"识别到：{text}，识别时间{recog_time:.2f}秒"
    
    temp_dir = tempfile.gettempdir()
    out_file = os.path.join(temp_dir, "real_time_speed_response.mp3")
    
    engine.save_to_file(response, out_file)
    engine.runAndWait()
    
    print(f"\n语音响应: {out_file}")
    
    # 保存报告
    report_file = os.path.join(temp_dir, "real_time_speed_result.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=== 实时语音识别速度测试结果 ===\n\n")
        f.write(f"测试音频: {audio_path}\n")
        f.write(f"QQ ASR: {qq_asr}\n")
        f.write(f"Whisper识别: {text}\n")
        f.write(f"识别时间: {recog_time:.2f}秒\n")
        f.write(f"速度评级: {rating}\n")
        f.write(f"相似度: {similarity:.1f}%\n")
        f.write(f"优化提升: {improvement:.1f}倍\n")
        f.write(f"语音响应: {out_file}\n")
    
    print(f"测试报告: {report_file}")
    
else:
    print("音频文件不存在")