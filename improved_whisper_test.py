#!/usr/bin/env python3
# 改进的Whisper测试 - 尝试不同参数
import os
import tempfile
import sys

def test_whisper_with_params(audio_path, model_size="base", params=None):
    """使用不同参数测试Whisper"""
    print(f"\n=== 测试参数: {params or '默认'} ===")
    
    try:
        import whisper
        
        # 加载模型
        print(f"加载模型: {model_size}")
        model = whisper.load_model(model_size)
        
        # 默认参数
        default_params = {
            "language": "zh",
            "task": "transcribe",
            "fp16": False,  # CPU不支持FP16
            "verbose": False
        }
        
        # 合并参数
        if params:
            default_params.update(params)
        
        print(f"识别参数: {default_params}")
        
        # 识别
        result = model.transcribe(audio_path, **default_params)
        
        # 分析结果
        text = result['text'].strip()
        language = result['language']
        
        print(f"识别文本: {text}")
        print(f"识别语言: {language}")
        
        if 'segments' in result and result['segments']:
            first_seg = result['segments'][0]
            print(f"第一段: {first_seg['text']} ({first_seg['start']:.1f}s-{first_seg['end']:.1f}s)")
        
        return {
            "text": text,
            "language": language,
            "params": default_params
        }
        
    except Exception as e:
        print(f"识别错误: {e}")
        return None

def main():
    print("=== 语音识别参数优化测试 ===")
    
    # 新音频文件
    audio_path = r"C:\Users\Administrator\.openclaw\qqbot\downloads\fca6ab22012bea2e558b4208f531f935.bin"
    qq_asr = "喂喂喂，你在吗？"
    
    print(f"测试音频: {audio_path}")
    print(f"QQ平台ASR: {qq_asr}")
    
    if not os.path.exists(audio_path):
        print("音频文件不存在")
        return
    
    file_size = os.path.getsize(audio_path)
    print(f"文件大小: {file_size} 字节")
    
    # 测试不同参数组合
    test_cases = [
        {"name": "默认参数", "params": None},
        {"name": "强制中文", "params": {"language": "zh", "task": "transcribe"}},
        {"name": "翻译模式", "params": {"language": "zh", "task": "translate"}},
        {"name": "详细输出", "params": {"verbose": True}},
        {"name": "温度调整", "params": {"temperature": 0.2}},  # 更确定性
        {"name": "无温度采样", "params": {"temperature": 0.0, "best_of": 5}},
    ]
    
    results = []
    
    for test_case in test_cases:
        result = test_whisper_with_params(
            audio_path, 
            model_size="base",
            params=test_case["params"]
        )
        
        if result:
            result["test_name"] = test_case["name"]
            results.append(result)
    
    # 分析结果
    print("\n" + "="*50)
    print("=== 参数优化结果分析 ===")
    
    best_result = None
    best_similarity = 0
    
    for result in results:
        text = result["text"]
        
        # 简单相似度计算
        similarity = 0
        if text and qq_asr:
            # 计算字符匹配
            matches = sum(1 for a, b in zip(text, qq_asr) if a == b)
            similarity = matches / max(len(text), len(qq_asr)) * 100
        
        print(f"\n{result['test_name']}:")
        print(f"  识别: {text}")
        print(f"  相似度: {similarity:.1f}%")
        
        # 检查是否包含关键信息
        keywords = ["在吗", "你在", "喂喂喂"]
        keyword_found = any(keyword in text for keyword in keywords)
        print(f"  关键信息: {'✅' if keyword_found else '❌'}")
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_result = result
    
    # 生成最佳结果的语音响应
    if best_result:
        print(f"\n=== 最佳参数: {best_result['test_name']} ===")
        print(f"最佳识别: {best_result['text']}")
        print(f"最佳相似度: {best_similarity:.1f}%")
        
        # 生成语音响应
        import pyttsx3
        
        response_text = f"语音识别优化测试完成，最佳参数{best_result['test_name']}，识别内容：{best_result['text'][:30]}..."
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 0.9)
        
        temp_dir = tempfile.gettempdir()
        response_file = os.path.join(temp_dir, "improved_response.mp3")
        
        engine.save_to_file(response_text, response_file)
        engine.runAndWait()
        
        if os.path.exists(response_file):
            print(f"\n语音响应生成: {response_file}")
            
            # 保存优化报告
            report_file = os.path.join(temp_dir, "parameter_optimization_report.txt")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("=== Whisper参数优化测试报告 ===\n\n")
                f.write(f"测试音频: {audio_path}\n")
                f.write(f"文件大小: {file_size} 字节\n")
                f.write(f"QQ平台ASR: {qq_asr}\n\n")
                
                f.write("=== 参数测试结果 ===\n")
                for result in results:
                    text = result["text"]
                    similarity = 0
                    if text and qq_asr:
                        matches = sum(1 for a, b in zip(text, qq_asr) if a == b)
                        similarity = matches / max(len(text), len(qq_asr)) * 100
                    
                    f.write(f"\n{result['test_name']}:\n")
                    f.write(f"  识别文本: {text}\n")
                    f.write(f"  相似度: {similarity:.1f}%\n")
                    f.write(f"  参数: {result['params']}\n")
                
                f.write(f"\n=== 最佳参数 ===\n")
                f.write(f"名称: {best_result['test_name']}\n")
                f.write(f"识别: {best_result['text']}\n")
                f.write(f"相似度: {best_similarity:.1f}%\n")
                f.write(f"参数: {best_result['params']}\n")
                f.write(f"\n语音响应: {response_file}\n")
            
            print(f"优化报告: {report_file}")
            print(f"语音文件: {response_file}")
            
            return response_file
    
    return None

if __name__ == "__main__":
    result_file = main()
    if result_file:
        print(f"\n✅ 参数优化测试完成，语音响应: {result_file}")
    else:
        print("\n❌ 参数优化测试失败")