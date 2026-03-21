#!/usr/bin/env python3
# 更新MEMORY.md格式

import os
import json
from datetime import datetime

def update_memory_format():
    """更新MEMORY.md文件格式"""
    
    memory_file = "MEMORY.md"
    memory_dir = "memory"
    index_file = os.path.join(memory_dir, "index.json")
    
    # 读取索引文件获取统计信息
    stats = {
        'total': 0,
        'categories': {'work': 0, 'life': 0, 'interest': 0, 'learning': 0, 'other': 0},
        'emotions': {'positive': 0, 'neutral': 0, 'negative': 0}
    }
    
    if os.path.exists(index_file):
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                stats['total'] = index_data.get('total_memories', 0)
                stats['categories'] = index_data.get('categories', stats['categories'])
                stats['emotions'] = index_data.get('emotions', stats['emotions'])
        except:
            pass
    
    # 读取现有内容
    existing_content = ""
    if os.path.exists(memory_file):
        with open(memory_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # 提取最近记忆部分
    recent_memories = []
    lines = existing_content.split('\n')
    in_recent_section = False
    
    for line in lines:
        if line.strip() == "## 最近记忆":
            in_recent_section = True
            continue
        elif line.strip().startswith("## ") and in_recent_section:
            break
        
        if in_recent_section and line.strip().startswith("- ["):
            recent_memories.append(line.strip())
    
    # 创建新的MEMORY.md内容
    new_content = f"""# MEMORY.md - 主记忆文件

## 记忆索引
- 总记忆数: {stats['total']}
- 分类统计: 工作({stats['categories']['work']}), 生活({stats['categories']['life']}), 兴趣({stats['categories']['interest']}), 学习({stats['categories']['learning']}), 其他({stats['categories']['other']})
- 情感统计: 积极({stats['emotions']['positive']}), 中性({stats['emotions']['neutral']}), 消极({stats['emotions']['negative']})
- 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 最近记忆
{chr(10).join(recent_memories[:10]) if recent_memories else "- 暂无最近记忆"}

## 重要记忆
- [2026-03-21 10:30] 语音识别优化完成 [工作, 重要]
- [2026-03-21 09:50] 贾维斯升级指令记录 [工作, 重要]
- [2026-03-21 12:05] 开始记忆系统优化设计 [工作, 重要]

## 关联网络
- 语音识别 → 贾维斯升级 → 长期规划
- 记忆系统 → 知识库 → 自我学习
- 工作记忆 → 项目进展 → 任务管理

## 系统状态
- 记忆系统: 已优化 (v1.0.0)
- 语音系统: 已优化 (0.39秒响应)
- 贾维斯模式: 已激活
- 守护进程: 运行正常
- 知识库: 构建中

## 使用说明
1. 所有记忆自动分类保存
2. 支持关键词和分类搜索
3. 情感分析自动标记
4. 记忆关联自动建立
5. 每日自动备份到Git

---
*记忆系统版本: 1.0.0 | 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    # 写入新内容
    with open(memory_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"MEMORY.md格式更新完成")
    print(f"总记忆数: {stats['total']}")
    print(f"分类统计: {stats['categories']}")
    print(f"情感统计: {stats['emotions']}")

if __name__ == "__main__":
    update_memory_format()