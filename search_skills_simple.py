#!/usr/bin/env python3
# 搜索OpenClaw技能 - 简化版

import subprocess
import json

def main():
    print("搜索OpenClaw技能库...")
    
    # 要搜索的技能名称
    target_skills = [
        "voice-wakeup",
        "long-term-memory", 
        "jarvis-core",
        "persistent-agent",
        "self-learning"
    ]
    
    print(f"目标技能: {', '.join(target_skills)}")
    print()
    
    # 运行技能列表命令
    try:
        result = subprocess.run(
            ["openclaw", "skills", "list"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            output = result.stdout
            
            found = []
            not_found = []
            
            # 简单文本搜索
            for skill in target_skills:
                if skill.lower() in output.lower():
                    found.append(skill)
                else:
                    not_found.append(skill)
            
            print("找到的技能:")
            for skill in found:
                print(f"  - {skill}")
            
            print("\n未找到的技能:")
            for skill in not_found:
                print(f"  - {skill}")
            
            # 检查现有的语音相关技能
            print("\n现有的语音相关技能:")
            voice_keywords = ["voice", "语音", "tts", "stt", "sag", "whisper", "sherpa"]
            for line in output.split('\n'):
                line_lower = line.lower()
                for keyword in voice_keywords:
                    if keyword in line_lower:
                        print(f"  - {line.strip()[:80]}")
                        break
            
            print("\n现有的记忆相关技能:")
            memory_keywords = ["memory", "记忆", "note", "笔记"]
            for line in output.split('\n'):
                line_lower = line.lower()
                for keyword in memory_keywords:
                    if keyword in line_lower:
                        print(f"  - {line.strip()[:80]}")
                        break
            
            return found, not_found
            
        else:
            print(f"命令执行失败")
            return [], target_skills
            
    except Exception as e:
        print(f"搜索失败: {e}")
        return [], target_skills

if __name__ == "__main__":
    print("=" * 50)
    print("技能搜索报告")
    print("=" * 50)
    
    found, not_found = main()
    
    print("\n" + "=" * 50)
    print(f"找到: {len(found)} 个技能")
    print(f"未找到: {len(not_found)} 个技能")
    
    if not_found:
        print("\n建议:")
        print("1. 这些技能可能不存在或名称不同")
        print("2. 使用替代方案实现相同功能")
        print("3. 检查技能商店或文档")
    
    print("=" * 50)