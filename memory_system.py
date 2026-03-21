#!/usr/bin/env python3
# 记忆系统优化 - 核心模块
# 版本: 1.0.0
# 创建: 2026-03-21
# 作者: 贾维斯升级项目

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib

class MemoryEntry:
    """记忆条目类"""
    
    def __init__(self, content: str, timestamp: Optional[str] = None):
        self.id = self._generate_id(content, timestamp)
        self.timestamp = timestamp or datetime.now().isoformat()
        self.content = content
        self.category = None  # 分类: work, life, interest, learning, other
        self.tags = []  # 关键词标签
        self.emotion = None  # 情感: positive, neutral, negative
        self.importance = 3  # 重要性: 1-5
        self.related_memories = []  # 相关记忆ID列表
        self.metadata = {}  # 额外元数据
    
    def _generate_id(self, content: str, timestamp: Optional[str]) -> str:
        """生成唯一ID"""
        if timestamp:
            base = f"{timestamp}:{content[:50]}"
        else:
            base = f"{datetime.now().isoformat()}:{content[:50]}"
        
        return f"mem_{hashlib.md5(base.encode()).hexdigest()[:8]}"
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'content': self.content,
            'category': self.category,
            'tags': self.tags,
            'emotion': self.emotion,
            'importance': self.importance,
            'related_memories': self.related_memories,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryEntry':
        """从字典创建"""
        memory = cls(data['content'], data['timestamp'])
        memory.id = data['id']
        memory.category = data['category']
        memory.tags = data['tags']
        memory.emotion = data['emotion']
        memory.importance = data['importance']
        memory.related_memories = data['related_memories']
        memory.metadata = data['metadata']
        return memory
    
    def __str__(self) -> str:
        return f"[{self.id}] {self.timestamp}: {self.content[:50]}... [{self.category}]"

class MemorySystem:
    """记忆系统主类"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.memory_dir = os.path.join(self.workspace_path, 'memory')
        self.categories_dir = os.path.join(self.memory_dir, 'categories')
        self.memories = []  # 当前加载的记忆
        self.index_file = os.path.join(self.memory_dir, 'index.json')
        self.graph_file = os.path.join(self.memory_dir, 'graph.json')
        
        # 确保目录存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保目录存在"""
        os.makedirs(self.memory_dir, exist_ok=True)
        os.makedirs(self.categories_dir, exist_ok=True)
        
        # 创建分类文件
        categories = ['work', 'life', 'interest', 'learning', 'other']
        for category in categories:
            category_file = os.path.join(self.categories_dir, f"{category}.md")
            if not os.path.exists(category_file):
                with open(category_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {category.upper()} 记忆\n\n")
                    f.write(f"最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    
    def add_memory(self, content: str, auto_classify: bool = True) -> MemoryEntry:
        """添加新记忆"""
        memory = MemoryEntry(content)
        
        if auto_classify:
            memory.category = self._classify_memory(content)
            memory.emotion = self._analyze_emotion(content)
            memory.tags = self._extract_tags(content)
        
        self.memories.append(memory)
        
        # 保存到文件
        self._save_memory_to_files(memory)
        self._update_index(memory)
        
        return memory
    
    def _classify_memory(self, content: str) -> str:
        """分类记忆"""
        # 关键词匹配
        work_keywords = ["项目", "任务", "工作", "会议", "deadline", "代码", "开发", "测试", "优化", "设计"]
        life_keywords = ["吃饭", "休息", "娱乐", "家庭", "朋友", "睡觉", "购物", "旅行", "健康", "运动"]
        interest_keywords = ["兴趣", "爱好", "游戏", "音乐", "电影", "阅读", "绘画", "摄影", "收藏", "手工"]
        learning_keywords = ["学习", "研究", "读书", "课程", "知识", "教育", "培训", "技能", "教程", "练习"]
        
        content_lower = content.lower()
        
        # 计算关键词出现次数
        work_count = sum(1 for word in work_keywords if word in content_lower)
        life_count = sum(1 for word in life_keywords if word in content_lower)
        interest_count = sum(1 for word in interest_keywords if word in content_lower)
        learning_count = sum(1 for word in learning_keywords if word in content_lower)
        
        counts = {
            'work': work_count,
            'life': life_count,
            'interest': interest_count,
            'learning': learning_count
        }
        
        # 找到最高分的分类
        max_category = max(counts, key=counts.get)
        
        # 如果所有分类都是0，返回'other'
        if counts[max_category] == 0:
            return 'other'
        
        return max_category
    
    def _analyze_emotion(self, content: str) -> str:
        """分析情感"""
        positive_words = ["好", "喜欢", "开心", "成功", "满意", "优秀", "完美", "高兴", "愉快", "棒"]
        negative_words = ["不好", "讨厌", "难过", "失败", "失望", "糟糕", "问题", "错误", "困难", "麻烦"]
        
        content_lower = content.lower()
        
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_tags(self, content: str) -> List[str]:
        """提取关键词标签"""
        # 简单实现：提取长度2-4的中文词
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,4}', content)
        
        # 去重并限制数量
        unique_words = list(set(chinese_words))
        return unique_words[:5]  # 最多5个标签
    
    def _save_memory_to_files(self, memory: MemoryEntry):
        """保存记忆到文件"""
        # 1. 保存到主记忆文件
        self._append_to_memory_file(memory)
        
        # 2. 保存到分类文件
        self._append_to_category_file(memory)
        
        # 3. 保存到每日记忆文件
        self._append_to_daily_file(memory)
    
    def _append_to_memory_file(self, memory: MemoryEntry):
        """追加到主记忆文件"""
        memory_file = os.path.join(self.workspace_path, 'MEMORY.md')
        
        # 读取现有内容
        existing_content = ""
        if os.path.exists(memory_file):
            with open(memory_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        
        # 找到最近记忆部分
        lines = existing_content.split('\n')
        recent_section_index = -1
        
        for i, line in enumerate(lines):
            if line.strip() == "## 最近记忆":
                recent_section_index = i
                break
        
        # 创建新的记忆条目
        memory_entry = f"- [{memory.timestamp[:10]} {memory.timestamp[11:16]}] {memory.content[:100]}... [{memory.category}]"
        if memory.emotion == 'positive':
            memory_entry += " 😊"
        elif memory.emotion == 'negative':
            memory_entry += " 😔"
        
        # 插入到最近记忆部分
        if recent_section_index != -1:
            lines.insert(recent_section_index + 2, memory_entry)
        else:
            # 如果没有最近记忆部分，添加到文件末尾
            lines.append("\n## 最近记忆")
            lines.append(memory_entry)
        
        # 写回文件
        with open(memory_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def _append_to_category_file(self, memory: MemoryEntry):
        """追加到分类文件"""
        if not memory.category:
            return
        
        category_file = os.path.join(self.categories_dir, f"{memory.category}.md")
        
        # 读取现有内容
        existing_content = ""
        if os.path.exists(category_file):
            with open(category_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        
        # 创建新的记忆条目
        memory_entry = f"- [{memory.timestamp[:10]} {memory.timestamp[11:16]}] {memory.content[:100]}..."
        if memory.tags:
            memory_entry += f" 标签: {', '.join(memory.tags[:3])}"
        
        # 添加到文件末尾
        with open(category_file, 'a', encoding='utf-8') as f:
            if not existing_content.endswith('\n'):
                f.write('\n')
            f.write(memory_entry + '\n')
    
    def _append_to_daily_file(self, memory: MemoryEntry):
        """追加到每日记忆文件"""
        date_str = memory.timestamp[:10]  # YYYY-MM-DD
        daily_file = os.path.join(self.memory_dir, f"{date_str}.md")
        
        # 读取现有内容
        existing_content = ""
        if os.path.exists(daily_file):
            with open(daily_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        
        # 创建新的记忆条目
        memory_entry = f"- [{memory.timestamp[11:16]}] {memory.content}"
        if memory.category:
            memory_entry += f" [{memory.category}]"
        
        # 添加到文件末尾
        with open(daily_file, 'a', encoding='utf-8') as f:
            if not existing_content:
                f.write(f"# {date_str} 记忆\n\n")
            elif not existing_content.endswith('\n'):
                f.write('\n')
            f.write(memory_entry + '\n')
    
    def _update_index(self, memory: MemoryEntry):
        """更新索引文件"""
        # 加载现有索引
        index_data = self._load_index()
        
        # 更新索引
        if 'memories' not in index_data:
            index_data['memories'] = []
        
        index_data['memories'].append({
            'id': memory.id,
            'timestamp': memory.timestamp,
            'category': memory.category,
            'emotion': memory.emotion,
            'importance': memory.importance
        })
        
        # 更新统计信息
        self._update_statistics(index_data, memory)
        
        # 保存索引
        self._save_index(index_data)
    
    def _load_index(self) -> Dict:
        """加载索引文件"""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 创建新的索引
        return {
            'total_memories': 0,
            'categories': {'work': 0, 'life': 0, 'interest': 0, 'learning': 0, 'other': 0},
            'emotions': {'positive': 0, 'neutral': 0, 'negative': 0},
            'last_updated': datetime.now().isoformat(),
            'memories': []
        }
    
    def _update_statistics(self, index_data: Dict, memory: MemoryEntry):
        """更新统计信息"""
        index_data['total_memories'] = len(index_data['memories'])
        
        # 更新分类统计
        if memory.category and memory.category in index_data['categories']:
            index_data['categories'][memory.category] += 1
        
        # 更新情感统计
        if memory.emotion and memory.emotion in index_data['emotions']:
            index_data['emotions'][memory.emotion] += 1
        
        index_data['last_updated'] = datetime.now().isoformat()
    
    def _save_index(self, index_data: Dict):
        """保存索引文件"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    def load_all_memories(self):
        """加载所有记忆"""
        # 从索引文件加载
        index_data = self._load_index()
        self.memories = []
        
        # 注意：这里简化实现，实际应该从各个文件加载完整内容
        # 目前只加载索引中的基本信息
        for mem_data in index_data.get('memories', []):
            memory = MemoryEntry("", mem_data['timestamp'])
            memory.id = mem_data['id']
            memory.category = mem_data['category']
            memory.emotion = mem_data['emotion']
            memory.importance = mem_data['importance']
            self.memories.append(memory)
        
        return self.memories
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        index_data = self._load_index()
        return {
            'total': index_data.get('total_memories', 0),
            'categories': index_data.get('categories', {}),
            'emotions': index_data.get('emotions', {}),
            'last_updated': index_data.get('last_updated', '')
        }
    
    def search_memories(self, keyword: str = None, category: str = None) -> List[MemoryEntry]:
        """搜索记忆"""
        results = []
        
        for memory in self.memories:
            match = True
            
            if keyword and keyword not in memory.content:
                match = False
            
            if category and memory.category != category:
                match = False
            
            if match:
                results.append(memory)
        
        return results

def main():
    """主函数 - 测试记忆系统"""
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
        print(f"  ✓ {memory}")
    
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

if __name__ == "__main__":
    main()