"""
简化版 Heartbeat 检查脚本
避免编码和路径问题
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

def check_projects():
    """检查项目目录"""
    projects = {
        "L_Intelligence": "E:\\L-Intelligence",
        "StockMonitor": "E:\\StockMonitor"
    }
    
    alerts = []
    for name, path in projects.items():
        if os.path.exists(path):
            print(f"[OK] 项目目录存在: {name} ({path})")
        else:
            print(f"[ERROR] 项目目录缺失: {name}")
            alerts.append(f"项目目录缺失: {name}")
    
    return alerts

def check_memory_file():
    """检查今天的 memory 文件"""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_dir = Path(__file__).parent / "memory"
    memory_file = memory_dir / f"{today}.md"
    
    alerts = []
    if not memory_file.exists():
        memory_dir.mkdir(parents=True, exist_ok=True)
        with open(memory_file, 'w', encoding='utf-8') as f:
            f.write(f"# {today}\n\n## Heartbeat 自动创建\n\n")
        print(f"[NOTE] 已自动创建今天的 memory 文件: {today}.md")
        alerts.append(f"已自动创建 memory 文件: {today}.md")
    else:
        print(f"[OK] 今天的 memory 文件已存在")
    
    return alerts

def check_gateway_status():
    """检查 Gateway 状态"""
    alerts = []
    try:
        # 使用shell执行命令
        result = subprocess.run(
            "openclaw gateway status",
            capture_output=True,
            text=True,
            timeout=10,
            shell=True
        )
        
        if "RPC 探测: 正常" in result.stdout:
            print("[OK] Gateway 状态正常")
        else:
            print("[WARN] Gateway 状态异常")
            alerts.append("Gateway 状态异常")
    except Exception as e:
        print(f"[ERROR] Gateway 检查失败")
        alerts.append("Gateway 检查失败")
    
    return alerts

def check_git_status():
    """检查 Git 状态"""
    alerts = []
    try:
        workspace = Path(__file__).parent
        os.chdir(workspace)
        
        result = subprocess.run(
            "git status",
            capture_output=True,
            text=True,
            timeout=10,
            shell=True
        )
        
        if "nothing to commit" in result.stdout:
            print("[OK] Git 工作区干净")
        else:
            print("[WARN] Git 有未提交文件")
            alerts.append("Git 有未提交文件")
    except Exception as e:
        print(f"[ERROR] Git 检查失败")
    
    return alerts

def main():
    """主函数"""
    print(f"Heartbeat 检查开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    all_alerts = []
    
    # 执行所有检查
    all_alerts.extend(check_projects())
    all_alerts.extend(check_memory_file())
    all_alerts.extend(check_gateway_status())
    all_alerts.extend(check_git_status())
    
    print("=" * 50)
    print(f"[OK] 检查完成，发现 {len(all_alerts)} 个问题")
    
    if all_alerts:
        print("\n需要关注的问题:")
        for i, alert in enumerate(all_alerts, 1):
            print(f"  {i}. {alert}")

if __name__ == "__main__":
    main()