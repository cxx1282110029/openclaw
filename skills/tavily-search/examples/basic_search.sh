#!/bin/bash
# Tavily Search 基本示例

echo "🔍 Tavily Search 示例脚本"
echo "========================"

# 检查环境变量
if [ -z "$TAVILY_API_KEY" ]; then
    echo "❌ 错误: 未设置 TAVILY_API_KEY 环境变量"
    echo "请设置环境变量: export TAVILY_API_KEY=your_api_key"
    echo "或从 https://tavily.com 获取 API 密钥"
    exit 1
fi

# 搜索查询
QUERY="${1:-人工智能最新发展}"

echo "搜索关键词: $QUERY"
echo ""

# 执行搜索
echo "执行搜索..."
curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$TAVILY_API_KEY\",
    \"query\": \"$QUERY\",
    \"search_depth\": \"basic\",
    \"include_answer\": true,
    \"include_raw_content\": false,
    \"max_results\": 3
  }" | jq '.'

echo ""
echo "搜索完成！"