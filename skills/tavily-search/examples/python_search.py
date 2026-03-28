#!/usr/bin/env python3
"""
Tavily Search Python 示例
"""

import os
import sys
import json
import requests
from typing import Dict, List, Optional

class TavilySearch:
    """Tavily Search API 客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("需要 Tavily API 密钥。请设置 TAVILY_API_KEY 环境变量或传入 api_key 参数")
        
        self.base_url = "https://api.tavily.com/search"
    
    def search(self, query: str, **kwargs) -> Dict:
        """执行搜索
        
        Args:
            query: 搜索关键词
            **kwargs: 额外参数
                - search_depth: "basic" 或 "advanced"
                - include_answer: bool, 是否包含 AI 答案
                - max_results: int, 最大结果数
                - time_range: "day", "week", "month", "year"
                
        Returns:
            搜索结果字典
        """
        data = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": kwargs.get("search_depth", "basic"),
            "include_answer": kwargs.get("include_answer", True),
            "include_raw_content": kwargs.get("include_raw_content", False),
            "max_results": kwargs.get("max_results", 5)
        }
        
        # 可选参数
        if "time_range" in kwargs:
            data["time_range"] = kwargs["time_range"]
        if "include_domains" in kwargs:
            data["include_domains"] = kwargs["include_domains"]
        if "exclude_domains" in kwargs:
            data["exclude_domains"] = kwargs["exclude_domains"]
        
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(self.base_url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "query": query}
    
    def print_results(self, results: Dict):
        """格式化打印搜索结果"""
        if "error" in results:
            print(f"搜索错误: {results['error']}")
            return
        
        print(f"搜索关键词: {results.get('query', '未知')}")
        print(f"响应时间: {results.get('response_time', 0):.2f}秒")
        print("")
        
        # AI 答案
        if "answer" in results:
            print("AI 答案:")
            print(f"   {results['answer']}")
            print("")
        
        # 搜索结果
        if "results" in results:
            print(f"找到 {len(results['results'])} 个结果:")
            print("-" * 60)
            
            for i, result in enumerate(results["results"], 1):
                print(f"{i}. {result.get('title', '无标题')}")
                print(f"   URL: {result.get('url', '无URL')}")
                print(f"   摘要: {result.get('content', '无内容')[:200]}...")
                if "score" in result:
                    print(f"   相关性: {result['score']:.2%}")
                print("")
        
        # 相关问题
        if "follow_up_questions" in results and results["follow_up_questions"]:
            print("相关问题:")
            for q in results["follow_up_questions"][:3]:
                print(f"   • {q}")
            print("")

def main():
    """主函数"""
    print("Tavily Search Python 示例")
    print("=" * 60)
    
    # 检查 API 密钥
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("❌ 错误: 未设置 TAVILY_API_KEY 环境变量")
        print("请设置环境变量: export TAVILY_API_KEY=your_api_key")
        print("或从 https://tavily.com 获取 API 密钥")
        return
    
    # 创建搜索客户端
    try:
        client = TavilySearch(api_key)
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    # 示例搜索
    queries = [
        "人工智能最新发展",
        "OpenAI GPT-5 最新消息",
        "机器学习在医疗诊断中的应用"
    ]
    
    for query in queries:
        print(f"\n🎯 搜索: {query}")
        print("-" * 40)
        
        # 执行搜索
        results = client.search(
            query=query,
            search_depth="basic",
            include_answer=True,
            max_results=3,
            time_range="month"  # 最近一个月
        )
        
        # 打印结果
        client.print_results(results)
        
        # 保存结果到文件
        output_file = f"tavily_results_{query[:10]}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"💾 结果已保存到: {output_file}")
        
        print("=" * 60)

if __name__ == "__main__":
    main()