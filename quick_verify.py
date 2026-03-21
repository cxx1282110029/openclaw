#!/usr/bin/env python3
import os, tempfile, time

audio_path = r"C:\Users\Administrator\.openclaw\qqbot\downloads\fbb212cc3b4014fefe76642992dd5397.bin"
qq_asr = "你属于哪个模型？"

print(f"测试: {audio_path}")
print(f"QQ ASR: {qq_asr}")

if os.path.exists(audio_path):
    import whisper
    start = time.time()
    
    model = whisper.load_model("small")
    result = model.transcribe(audio_path, language="zh", temperature=0.2)
    
    text = result['text'].strip()
    elapsed = time.time() - start
    
    print(f"\n识别结果: {text}")
    print(f"识别时间: {elapsed:.1f}秒")
    
    # 相似度
    matches = sum(1 for a, b in zip(text, qq_asr) if a == b)
    similarity = matches / max(len(text), len(qq_asr)) * 100
    print(f"相似度: {similarity:.1f}%")
    
    # 生成响应
    import pyttsx3
    engine = pyttsx3.init()
    
    if similarity > 50:
        response = f"优化验证成功！识别内容：{text}，相似度{similarity:.1f}%，准确率良好！"
    else:
        response = f"识别到：{text}，相似度{similarity:.1f}%，继续优化中"
    
    temp_dir = tempfile.gettempdir()
    out_file = os.path.join(temp_dir, "verify_response.mp3")
    
    engine.save_to_file(response, out_file)
    engine.runAndWait()
    
    print(f"\n语音响应: {out_file}")
    
    # 保存结果
    with open(os.path.join(temp_dir, "verify_report.txt"), 'w', encoding='utf-8') as f:
        f.write(f"测试音频: {audio_path}\n")
        f.write(f"QQ ASR: {qq_asr}\n")
        f.write(f"Whisper识别: {text}\n")
        f.write(f"相似度: {similarity:.1f}%\n")
        f.write(f"语音文件: {out_file}\n")
    
else:
    print("文件不存在")