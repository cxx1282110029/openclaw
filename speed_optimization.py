#!/usr/bin/env python3
# 语音识别响应速度优化
import os
import tempfile
import time
import threading

class FastSpeechRecognizer:
    """快速语音识别器 - 预加载模型优化"""
    
    def __init__(self, model_size="base"):
        """
        初始化识别器，预加载模型
        model_size: tiny(72MB), base(139MB), small(461MB)
        """
        print(f"初始化快速语音识别器，模型: {model_size}")
        
        self.model_size = model_size
        self.model = None
        self.model_loaded = False
        
        # 后台预加载模型
        self.load_thread = threading.Thread(target=self._preload_model)
        self.load_thread.daemon = True
        self.load_thread.start()
        
        # 识别缓存
        self.cache = {}
        self.cache_max_size = 100
        
    def _preload_model(self):
        """后台预加载模型"""
        try:
            import whisper
            print(f"后台预加载{self.model_size}模型...")
            start_time = time.time()
            
            self.model = whisper.load_model(self.model_size)
            load_time = time.time() - start_time
            
            self.model_loaded = True
            print(f"模型预加载完成，耗时: {load_time:.1f}秒")
            
        except Exception as e:
            print(f"模型加载失败: {e}")
    
    def wait_for_model(self, timeout=10):
        """等待模型加载完成"""
        if self.model_loaded:
            return True
            
        print(f"等待模型加载，最多{timeout}秒...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.model_loaded:
                return True
            time.sleep(0.1)
        
        print("模型加载超时")
        return False
    
    def recognize_fast(self, audio_path, use_cache=True):
        """
        快速语音识别
        use_cache: 是否使用缓存
        """
        if not self.wait_for_model():
            return "模型未就绪"
        
        # 检查缓存
        if use_cache:
            import hashlib
            with open(audio_path, 'rb') as f:
                audio_hash = hashlib.md5(f.read()).hexdigest()
            
            if audio_hash in self.cache:
                print(f"缓存命中: {audio_path}")
                return self.cache[audio_hash]
        
        # 开始识别
        start_time = time.time()
        
        try:
            # 使用优化参数
            result = self.model.transcribe(
                audio_path,
                language="zh",
                temperature=0.2,
                task="transcribe",
                verbose=False
            )
            
            text = result['text'].strip()
            recognition_time = time.time() - start_time
            
            print(f"识别完成: {text[:30]}... (耗时: {recognition_time:.1f}秒)")
            
            # 更新缓存
            if use_cache:
                if len(self.cache) >= self.cache_max_size:
                    # 移除最旧的缓存
                    oldest_key = next(iter(self.cache))
                    del self.cache[oldest_key]
                
                self.cache[audio_hash] = text
            
            return text
            
        except Exception as e:
            print(f"识别错误: {e}")
            return f"识别失败: {e}"
    
    def benchmark(self, audio_path, iterations=3):
        """性能基准测试"""
        print(f"\n=== 性能基准测试 ===")
        print(f"音频文件: {audio_path}")
        print(f"模型: {self.model_size}")
        print(f"迭代次数: {iterations}")
        
        if not os.path.exists(audio_path):
            print("音频文件不存在")
            return
        
        # 确保模型加载
        if not self.wait_for_model():
            print("模型未就绪")
            return
        
        times = []
        
        for i in range(iterations):
            print(f"\n第{i+1}次测试...")
            
            start_time = time.time()
            result = self.recognize_fast(audio_path, use_cache=(i>0))
            elapsed = time.time() - start_time
            
            times.append(elapsed)
            print(f"结果: {result[:30]}...")
            print(f"耗时: {elapsed:.2f}秒")
        
        # 统计分析
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n=== 性能统计 ===")
        print(f"平均耗时: {avg_time:.2f}秒")
        print(f"最快耗时: {min_time:.2f}秒")
        print(f"最慢耗时: {max_time:.2f}秒")
        print(f"缓存效果: 首次{times[0]:.2f}秒 vs 后续{sum(times[1:])/(len(times)-1):.2f}秒")
        
        return {
            "average": avg_time,
            "min": min_time,
            "max": max_time,
            "times": times
        }

def compare_models(audio_path):
    """比较不同模型的速度和准确率"""
    print("=== 模型速度对比测试 ===")
    
    models_to_test = [
        ("tiny", "72MB - 最快"),
        ("base", "139MB - 平衡"),
        ("small", "461MB - 最准")
    ]
    
    results = {}
    
    for model_size, description in models_to_test:
        print(f"\n测试模型: {model_size} ({description})")
        
        recognizer = FastSpeechRecognizer(model_size)
        
        # 等待模型加载
        if not recognizer.wait_for_model(timeout=30):
            print(f"{model_size}模型加载超时")
            continue
        
        # 单次识别测试
        start_time = time.time()
        result = recognizer.recognize_fast(audio_path, use_cache=False)
        elapsed = time.time() - start_time
        
        results[model_size] = {
            "time": elapsed,
            "result": result,
            "description": description
        }
        
        print(f"识别结果: {result[:30]}...")
        print(f"识别时间: {elapsed:.2f}秒")
    
    # 输出对比结果
    print("\n" + "="*50)
    print("=== 模型速度对比结果 ===")
    
    for model_size, data in results.items():
        print(f"\n{model_size}模型 ({data['description']}):")
        print(f"  识别时间: {data['time']:.2f}秒")
        print(f"  识别结果: {data['result'][:40]}...")
    
    # 推荐建议
    print("\n=== 优化建议 ===")
    fastest_model = min(results.items(), key=lambda x: x[1]['time'])
    print(f"最快模型: {fastest_model[0]} ({fastest_model[1]['time']:.2f}秒)")
    
    # 根据需求推荐
    if results.get('tiny') and results['tiny']['time'] < 1.0:
        print("推荐: tiny模型 - 速度最快，适合实时响应")
    elif results.get('base') and results['base']['time'] < 2.0:
        print("推荐: base模型 - 速度与准确率平衡")
    else:
        print("推荐: small模型 - 准确率最高，适合重要识别")
    
    return results

if __name__ == "__main__":
    # 测试音频
    test_audio = r"C:\Users\Administrator\.openclaw\qqbot\downloads\fbb212cc3b4014fefe76642992dd5397.bin"
    
    if os.path.exists(test_audio):
        print(f"测试音频: {test_audio}")
        
        # 方案1: 测试预加载优化
        print("\n" + "="*50)
        print("方案1: 预加载模型优化测试")
        
        recognizer = FastSpeechRecognizer("base")
        benchmark_result = recognizer.benchmark(test_audio, iterations=3)
        
        # 方案2: 模型对比
        print("\n" + "="*50)
        print("方案2: 不同模型速度对比")
        compare_results = compare_models(test_audio)
        
        # 生成优化报告
        temp_dir = tempfile.gettempdir()
        report_file = os.path.join(temp_dir, "speed_optimization_report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=== 语音识别响应速度优化报告 ===\n\n")
            f.write(f"测试音频: {test_audio}\n")
            f.write(f"文件大小: {os.path.getsize(test_audio)} 字节\n\n")
            
            f.write("=== 预加载优化测试 ===\n")
            if benchmark_result:
                f.write(f"平均耗时: {benchmark_result['average']:.2f}秒\n")
                f.write(f"最快耗时: {benchmark_result['min']:.2f}秒\n")
                f.write(f"最慢耗时: {benchmark_result['max']:.2f}秒\n")
                f.write(f"缓存效果: 首次{benchmark_result['times'][0]:.2f}秒 vs 后续{sum(benchmark_result['times'][1:])/(len(benchmark_result['times'])-1):.2f}秒\n\n")
            
            f.write("=== 模型速度对比 ===\n")
            for model_size, data in compare_results.items():
                f.write(f"\n{model_size}模型:\n")
                f.write(f"  识别时间: {data['time']:.2f}秒\n")
                f.write(f"  识别结果: {data['result']}\n")
            
            f.write("\n=== 优化建议 ===\n")
            f.write("1. 使用预加载模型避免重复加载\n")
            f.write("2. 根据需求选择模型大小\n")
            f.write("3. 启用缓存减少重复计算\n")
            f.write("4. 考虑使用tiny模型获得最快响应\n")
        
        print(f"\n优化报告: {report_file}")
        
    else:
        print(f"测试音频不存在: {test_audio}")