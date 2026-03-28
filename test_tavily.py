#!/usr/bin/env python3
"""
测试 Tavily API
"""

import requests
import json

# 你的 API 密钥
API_KEY = "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"

def test_tavily():
    """测试 Tavily API"""
    print("测试 Tavily API...")
    
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    
    # 测试数据
    test_query = "人工智能最新发展"
    
    data = {
        "api_key": API_KEY,
        "query": test_query,
        "search_depth": "basic",
        "include_answer": True,
        "max_results": 3
    }
    
    try:
        print(f"搜索: {test_query}")
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            print(f"状态: 成功 (响应时间: {results.get('response_time', 0):.2f}秒)")
            print(f"查询: {results.get('query', '未知')}")
            
            if "answer" in results:
                print(f"\nAI 答案: {results['answer'][:200]}...")
            
            if "results" in results:
                print(f"\n找到 {len(results['results'])} 个结果:")
                for i, result in enumerate(results["results"], 1):
                    print(f"\n{i}. {result.get('title', '无标题')}")
                    print(f"   链接: {result.get('url', '无URL')}")
                    print(f"   摘要: {result.get('content', '无内容')[:150]}...")
            
            # 保存结果
            with open("tavily_test_result.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n结果已保存到: tavily_test_result.json")
            
            return True
        else:
            print(f"错误: HTTP {response.status_code}")
            print(f"响应: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"API 调用失败: {e}")
        return False

if __name__ == "__main__":
    success = test_tavily()
    if success:
        print("\n✅ Tavily API 测试成功！")
    else:
        print("\n❌ Tavily API 测试失败")