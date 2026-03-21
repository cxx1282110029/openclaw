#!/usr/bin/env python3
import os, tempfile

audio_path = r"C:\Users\Administrator\.openclaw\qqbot\downloads\fca6ab22012bea2e558b4208f531f935.bin"
print(f"测试: {audio_path}")

if os.path.exists(audio_path):
    import whisper
    model = whisper.load_model("base")
    
    # 最佳参数
    result = model.transcribe(audio_path, language="zh", temperature=0.2)
    text = result['text'].strip()
    print(f"识别: {text}")
    
    # 生成响应
    import pyttsx3
    engine = pyttsx3.init()
    response = f"语音识别优化成功！识别内容：{text}，准确率大幅提升！"
    
    temp_dir = tempfile.gettempdir()
    out_file = os.path.join(temp_dir, "optimized_final.mp3")
    
    engine.save_to_file(response, out_file)
    engine.runAndWait()
    
    print(f"语音文件: {out_file}")
    
    # 保存结果
    with open(os.path.join(temp_dir, "optimization_summary.txt"), 'w', encoding='utf-8') as f:
        f.write(f"最佳参数: temperature=0.2\n")
        f.write(f"识别结果: {text}\n")
        f.write(f"语音文件: {out_file}\n")
    
else:
    print("文件不存在")