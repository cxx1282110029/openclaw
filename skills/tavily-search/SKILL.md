---
name: Tavily Search
description: 使用 Tavily AI 搜索 API 进行智能网络搜索。Tavily 提供 AI 优化的搜索结果，特别适合 AI 助手和自动化任务。
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["curl","jq"]},"install":[{"id":"tavily","kind":"api","label":"获取 Tavily API 密钥 (https://tavily.com)"}]}}
---

# Tavily Search Skill

## 描述
Tavily Search 是一个 AI 优化的搜索 API，专门为 AI 助手和自动化任务设计。它提供更相关、更结构化的搜索结果。

## 功能特点
- **AI 优化搜索**: 结果经过 AI 筛选和排序
- **结构化数据**: 返回简洁、相关的信息
- **实时搜索**: 获取最新网络信息
- **多语言支持**: 支持中文搜索
- **API 集成**: 简单的 REST API 调用

## 安装要求
1. **Tavily API 密钥**: 从 https://tavily.com 注册获取
2. **curl**: 用于 API 调用
3. **jq**: 用于 JSON 处理（可选）

## 配置
在环境变量或配置文件中设置 Tavily API 密钥：
```bash
export TAVILY_API_KEY="your_api_key_here"
```

或者在 `~/.openclaw/openclaw.json` 中添加：
```json
{
  "tavily": {
    "apiKey": "your_api_key_here"
  }
}
```

## 使用方法

### 基本搜索
```bash
# 使用 curl 搜索
curl -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "$TAVILY_API_KEY",
    "query": "人工智能最新发展",
    "search_depth": "basic",
    "include_answer": true,
    "include_raw_content": false,
    "max_results": 5
  }'
```

### 高级搜索选项
```json
{
  "query": "搜索关键词",
  "search_depth": "basic|advanced",  // 搜索深度
  "include_answer": true,           // 是否包含 AI 生成的答案
  "include_raw_content": false,     // 是否包含原始内容
  "max_results": 5,                 // 最大结果数
  "include_domains": [],            // 包含的域名
  "exclude_domains": [],            // 排除的域名
  "time_range": "day|week|month|year"  // 时间范围
}
```

### Python 示例
```python
import requests
import os

def tavily_search(query, api_key=None):
    if api_key is None:
        api_key = os.getenv("TAVILY_API_KEY")
    
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    data = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": True,
        "max_results": 5
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# 使用示例
results = tavily_search("OpenAI GPT-5 最新消息")
print(results)
```

### Shell 脚本示例
```bash
#!/bin/bash
# tavily_search.sh

TAVILY_API_KEY="${TAVILY_API_KEY:-$1}"
QUERY="${2:-人工智能}"

if [ -z "$TAVILY_API_KEY" ]; then
    echo "错误: 需要 Tavily API 密钥"
    echo "用法: $0 <api_key> [查询关键词]"
    exit 1
fi

curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$TAVILY_API_KEY\",
    \"query\": \"$QUERY\",
    \"search_depth\": \"basic\",
    \"include_answer\": true,
    \"max_results\": 3
  }" | jq '.'
```

## 返回结果格式
```json
{
  "query": "搜索关键词",
  "answer": "AI 生成的简要答案",
  "results": [
    {
      "title": "结果标题",
      "url": "结果URL",
      "content": "结果摘要",
      "score": 0.95
    }
  ],
  "response_time": 1.23,
  "images": ["图片URL"],
  "follow_up_questions": ["相关问题"]
}
```

## 使用场景

### 1. AI 助手增强
```bash
# 为 AI 助手提供实时信息
tavily_search "今天北京天气如何"
```

### 2. 研究辅助
```bash
# 学术研究
tavily_search "机器学习在医疗诊断中的应用 2024"
```

### 3. 新闻监控
```bash
# 获取最新新闻
tavily_search "科技行业最新融资新闻" "time_range": "day"
```

### 4. 竞争分析
```bash
# 竞争对手信息
tavily_search "OpenAI 最新产品发布"
```

## 最佳实践

### 查询优化
1. **具体明确**: 使用具体的搜索词
2. **中文优先**: Tavily 对中文支持良好
3. **限制范围**: 使用时间范围和域名过滤
4. **结果数量**: 根据需求调整 max_results

### 错误处理
```python
try:
    results = tavily_search(query)
    if "error" in results:
        print(f"搜索错误: {results['error']}")
    else:
        # 处理结果
        pass
except Exception as e:
    print(f"API 调用失败: {e}")
```

### 速率限制
- 免费版: 1000 次搜索/月
- 专业版: 更高限制
- 建议添加延迟避免超限

## 与其他搜索工具对比

| 特性 | Tavily | 传统搜索 | 其他 AI 搜索 |
|------|--------|----------|--------------|
| AI 优化 | ✅ | ❌ | ✅ |
| 结构化结果 | ✅ | ❌ | ⚠️ |
| 实时性 | ✅ | ✅ | ⚠️ |
| 中文支持 | ✅ | ✅ | ⚠️ |
| 成本 | 免费层可用 | 免费 | 通常付费 |

## 故障排除

### 常见问题
1. **API 密钥无效**: 检查密钥是否正确，是否已激活
2. **速率限制**: 免费版每月 1000 次搜索
3. **网络问题**: 检查网络连接和防火墙
4. **JSON 解析错误**: 确保安装了 jq 或使用正确的 JSON 解析

### 调试命令
```bash
# 测试 API 连接
curl -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "test", "query": "test"}' \
  -v

# 检查环境变量
echo "TAVILY_API_KEY: ${TAVILY_API_KEY:0:10}..."
```

## 资源链接
- [Tavily 官网](https://tavily.com)
- [API 文档](https://docs.tavily.com)
- [Python SDK](https://github.com/tavily-ai/tavily-python)
- [定价页面](https://tavily.com/pricing)

## 更新日志
- v1.0.0: 初始版本，包含基本搜索功能
- v1.1.0: 添加高级搜索选项和错误处理

---

**注意**: 使用 Tavily Search 需要注册并获取 API 密钥。免费版提供每月 1000 次搜索。