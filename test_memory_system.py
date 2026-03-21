#!/usr/bin/env python3
# 记忆系统测试脚本

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory_system import MemorySystem

def main():
    print("记忆系统测试开始")
    print("=" * 50)
    
    # 创建记忆系统实例
    memory_system = MemorySystem()
    
    # 测试添加记忆
    test_memories = [
        "今天开始实施记忆系统优化设计，按照7天计划执行",
        "用户确认接受替代方案，贾维斯升级完成",
        "晚上准备吃火锅，和朋友一起聚餐",
        "学习新的Python机器学习算法，准备应用到项目中",
        "玩了一款新的游戏，画面和剧情都很棒"
    ]
    
    print("添加测试记忆...")
    for content in test_memories:
        memory = memory_system.add_memory(content)
        print(f"  [OK] {memory}")
    
    # 获取统计信息
    stats = memory_system.get_statistics()
    print("\n记忆统计:")
    print(f"  总记忆数: {stats['total']}")
    print(f"  分类统计: {stats['categories']}")
    print(f"  情感统计: {stats['emotions']}")
    
    # 测试搜索
    print("\n搜索测试:")
    work_memories = memory_system.search_memories(category='work')
    print(f"  工作相关记忆: {len(work_memories)} 条")
    
    print("\n记忆系统测试完成")
    
    # 显示创建的文件
    print("\n创建的文件:")
    memory_dir = os.path.join(os.getcwd(), 'memory')
    if os.path.exists(memory_dir):
        for root, dirs, files in os.walk(memory_dir):
            for file in files:
                filepath = os.path.join(root, file)
                print(f"  - {os.path.relpath(filepath, os.getcwd())}")

if __name__ == "__main__":
    main()