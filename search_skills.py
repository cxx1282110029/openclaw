#!/usr/bin/env python3
# 搜索OpenClaw技能

import subprocess
import json
import re

def search_skills():
    """搜索技能"""
    
    print("🔍 搜索OpenClaw技能库...")
    
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
            ["openclaw", "skills", "list", "--json"],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            # 解析JSON输出
            try:
                skills_data = json.loads(result.stdout)
                print(f"找到 {len(skills_data)} 个技能")
                
                found_skills = []
                not_found_skills = []
                
                for skill in skills_data:
                    skill_name = skill.get('skill', '').lower()
                    skill_desc = skill.get('description', '').lower()
                    
                    # 检查是否匹配目标技能
                    for target in target_skills:
                        if target in skill_name or target in skill_desc:
                            found_skills.append({
                                'name': skill.get('skill', ''),
                                'status': skill.get('status', ''),
                                'description': skill.get('description', ''),
                                'source': skill.get('source', '')
                            })
                            break
                
                # 检查哪些技能没找到
                for target in target_skills:
                    found = False
                    for skill in found_skills:
                        if target in skill['name'].lower() or target in skill['description'].lower():
                            found = True
                            break
                    if not found:
                        not_found_skills.append(target)
                
                print("\n✅ 找到的技能:")
                for skill in found_skills:
                    print(f"  • {skill['name']} ({skill['status']})")
                    print(f"    描述: {skill['description'][:100]}...")
                    print(f"    来源: {skill['source']}")
                    print()
                
                print("\n❌ 未找到的技能:")
                for skill in not_found_skills:
                    print(f"  • {skill}")
                    
                return found_skills, not_found_skills
                
            except json.JSONDecodeError:
                print("无法解析JSON输出，尝试文本搜索...")
                # 回退到文本搜索
                return search_text(result.stdout, target_skills)
                
        else:
            print(f"命令执行失败: {result.stderr}")
            return [], target_skills
            
    except Exception as e:
        print(f"搜索失败: {e}")
        return [], target_skills

def search_text(output_text, target_skills):
    """文本搜索"""
    print("📄 进行文本搜索...")
    
    found_skills = []
    not_found_skills = target_skills.copy()
    
    lines = output_text.split('\n')
    for line in lines:
        line_lower = line.lower()
        for target in target_skills:
            if target in line_lower:
                if target not in [s['target'] for s in found_skills]:
                    found_skills.append({
                        'target': target,
                        'line': line.strip()[:100]
                    })
                    if target in not_found_skills:
                        not_found_skills.remove(target)
    
    print("\n✅ 文本匹配到的技能:")
    for skill in found_skills:
        print(f"  • {skill['target']}")
        print(f"    匹配行: {skill['line']}")
        print()
    
    print("\n❌ 完全未找到的技能:")
    for skill in not_found_skills:
        print(f"  • {skill}")
    
    return found_skills, not_found_skills

if __name__ == "__main__":
    print("=" * 60)
    print("贾维斯升级指令 - 技能搜索报告")
    print("=" * 60)
    
    found, not_found = search_skills()
    
    print("\n" + "=" * 60)
    print("搜索总结:")
    print(f"✅ 找到: {len(found)} 个技能")
    print(f"❌ 未找到: {len(not_found)} 个技能")
    
    if not_found:
        print("\n💡 建议:")
        print("1. 使用替代方案实现功能")
        print("2. 检查技能名称是否正确")
        print("3. 使用ClawdHub搜索更多技能")
        print("4. 考虑自定义技能开发")
    
    print("=" * 60)