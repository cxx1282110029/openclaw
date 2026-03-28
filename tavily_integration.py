#!/usr/bin/env python3
"""
Tavily Search 集成模块
将 Tavily 搜索功能集成到现有自动化工作流中
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional

class TavilyIntegration:
    """Tavily Search 集成类"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY", "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")
        self.base_url = "https://api.tavily.com/search"
        self.search_history = []
        
    def search(self, query: str, **kwargs) -> Dict:
        """执行搜索并记录历史"""
        data = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": kwargs.get("search_depth", "basic"),
            "include_answer": kwargs.get("include_answer", True),
            "max_results": kwargs.get("max_results", 3)
        }
        
        # 可选参数
        optional_params = ["time_range", "include_domains", "exclude_domains"]
        for param in optional_params:
            if param in kwargs:
                data[param] = kwargs[param]
        
        headers = {"Content-Type": "application/json"}
        
        try:
            start_time = datetime.now()
            response = requests.post(self.base_url, json=data, headers=headers, timeout=30)
            response_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                results = response.json()
                
                # 记录搜索历史
                search_record = {
                    "timestamp": datetime.now().isoformat(),
                    "query": query,
                    "response_time": response_time,
                    "results_count": len(results.get("results", [])),
                    "success": True
                }
                self.search_history.append(search_record)
                
                # 保存历史记录
                self._save_history()
                
                return results
            else:
                # 记录错误
                error_record = {
                    "timestamp": datetime.now().isoformat(),
                    "query": query,
                    "error": f"HTTP {response.status_code}",
                    "success": False
                }
                self.search_history.append(error_record)
                self._save_history()
                
                return {"error": f"HTTP {response.status_code}", "response_text": response.text[:200]}
                
        except Exception as e:
            error_record = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "error": str(e),
                "success": False
            }
            self.search_history.append(error_record)
            self._save_history()
            
            return {"error": str(e)}
    
    def _save_history(self):
        """保存搜索历史"""
        history_file = "tavily_search_history.json"
        try:
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(self.search_history, f, ensure_ascii=False, indent=2)
        except:
            pass  # 忽略保存错误
    
    def get_usage_stats(self) -> Dict:
        """获取使用统计"""
        if not self.search_history:
            return {"total_searches": 0, "success_rate": 0, "avg_response_time": 0}
        
        total = len(self.search_history)
        successful = sum(1 for record in self.search_history if record.get("success", False))
        response_times = [r.get("response_time", 0) for r in self.search_history if "response_time" in r]
        
        return {
            "total_searches": total,
            "successful_searches": successful,
            "success_rate": successful / total if total > 0 else 0,
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
            "last_search": self.search_history[-1]["timestamp"] if self.search_history else None
        }
    
    def batch_search(self, queries: List[str], **kwargs) -> List[Dict]:
        """批量搜索多个查询"""
        results = []
        for query in queries:
            print(f"搜索: {query}")
            result = self.search(query, **kwargs)
            results.append({"query": query, "result": result})
        return results

# 集成到自动化工作流的示例函数
def integrate_with_automation():
    """将 Tavily 集成到自动化工作流"""
    print("将 Tavily Search 集成到自动化工作流...")
    
    # 创建集成实例
    tavily = TavilyIntegration()
    
    # 示例：为自动化表单填写提供数据
    def get_form_autofill_data(topic: str) -> Dict:
        """获取表单自动填写数据"""
        print(f"为 '{topic}' 获取自动填写数据...")
        
        # 搜索相关信息
        results = tavily.search(f"{topic} 最新信息", max_results=2)
        
        if "error" in results:
            return {"error": results["error"], "suggestions": []}
        
        # 提取建议数据
        suggestions = []
        if "results" in results:
            for result in results["results"][:2]:
                suggestion = {
                    "title": result.get("title", ""),
                    "summary": result.get("content", "")[:100],
                    "source": result.get("url", "")
                }
                suggestions.append(suggestion)
        
        return {
            "topic": topic,
            "ai_answer": results.get("answer", "未找到相关信息"),
            "suggestions": suggestions,
            "search_time": results.get("response_time", 0)
        }
    
    # 示例：监控特定主题
    def monitor_topic(topic: str, interval_hours: int = 24):
        """监控特定主题的最新动态"""
        print(f"开始监控主题: {topic} (每{interval_hours}小时)")
        
        # 搜索最新信息
        results = tavily.search(
            f"{topic} 最新动态",
            time_range="day",
            max_results=3
        )
        
        if "error" in results:
            print(f"监控失败: {results['error']}")
            return None
        
        # 提取监控结果
        monitoring_result = {
            "topic": topic,
            "monitor_time": datetime.now().isoformat(),
            "new_articles": len(results.get("results", [])),
            "latest_articles": []
        }
        
        for result in results.get("results", []):
            article = {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "summary": result.get("content", "")[:150],
                "published": "今天"  # 实际应用中应该解析发布时间
            }
            monitoring_result["latest_articles"].append(article)
        
        return monitoring_result
    
    # 返回集成函数
    return {
        "get_form_autofill_data": get_form_autofill_data,
        "monitor_topic": monitor_topic,
        "tavily_instance": tavily
    }

if __name__ == "__main__":
    print("Tavily Search 集成测试")
    print("=" * 50)
    
    # 测试集成
    integration = integrate_with_automation()
    
    # 测试表单自动填写数据获取
    print("\n1. 测试表单自动填写数据获取:")
    form_data = integration["get_form_autofill_data"]("人工智能")
    print(f"   获取到 {len(form_data.get('suggestions', []))} 条建议")
    
    # 测试主题监控
    print("\n2. 测试主题监控:")
    monitor_result = integration["monitor_topic"]("机器学习")
    if monitor_result:
        print(f"   发现 {monitor_result['new_articles']} 篇新文章")
    
    # 显示使用统计
    print("\n3. 使用统计:")
    stats = integration["tavily_instance"].get_usage_stats()
    print(f"   总搜索次数: {stats['total_searches']}")
    print(f"   成功率: {stats['success_rate']:.1%}")
    print(f"   平均响应时间: {stats['avg_response_time']:.2f}秒")
    
    print("\n✅ Tavily Search 集成完成！")