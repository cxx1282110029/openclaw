#!/usr/bin/env python3
# 下载Whisper small模型提升准确率
import whisper
import time

print("=== 下载Whisper small模型提升准确率 ===")
print("模型大小: 461MB (比base模型大3倍)")
print("预计准确率提升: 30-50%")
print("下载时间: 约2-3分钟")

try:
    print("\n开始下载small模型...")
    start_time = time.time()
    
    # 加载small模型（首次会自动下载）
    model = whisper.load_model("small")
    
    end_time = time.time()
    download_time = end_time - start_time
    
    print(f"\n✅ small模型下载成功！")
    print(f"下载时间: {download_time:.1f}秒")
    print(f"模型大小: 461MB")
    print(f"预计准确率: 比base模型高30-50%")
    
    # 测试模型
    print("\n测试small模型识别...")
    
    # 使用之前的测试音频
    test_audio = r"C:\Users\Administrator\.openclaw\qqbot\downloads\fca6ab22012bea2e558b4208f531f935.bin"
    
    import os
    if os.path.exists(test_audio):
        print(f"使用测试音频: {test_audio}")
        
        # 使用优化参数
        result = model.transcribe(
            test_audio,
            language="zh",
            temperature=0.2,
            task="transcribe"
        )
        
        text = result['text'].strip()
        print(f"small模型识别结果: {text}")
        print(f"识别语言: {result['language']}")
        
        # 与base模型对比
        print("\n=== 模型对比 ===")
        print("base模型识别: '我们在哪里等你?'")
        print(f"small模型识别: '{text}'")
        
        # 保存结果
        import tempfile
        temp_dir = tempfile.gettempdir()
        result_file = os.path.join(temp_dir, "small_model_test.txt")
        
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write("=== Whisper small模型测试报告 ===\n\n")
            f.write(f"模型: small (461MB)\n")
            f.write(f"下载时间: {download_time:.1f}秒\n")
            f.write(f"测试音频: {test_audio}\n")
            f.write(f"参数: language=zh, temperature=0.2\n")
            f.write(f"识别结果: {text}\n")
            f.write(f"识别语言: {result['language']}\n")
            f.write(f"base模型对比: '我们在哪里等你?'\n")
            f.write(f"准确率评估: 待进一步测试验证\n")
        
        print(f"\n测试报告: {result_file}")
        
    else:
        print("测试音频不存在，跳过识别测试")
    
    print("\n🎯 small模型准备就绪，可以开始准确率提升测试！")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()