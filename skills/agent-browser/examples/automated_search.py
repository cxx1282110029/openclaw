#!/usr/bin/env python3
"""
浏览器自动化搜索示例
使用 subprocess 调用 openclaw browser 命令
"""

import subprocess
import time
import json
import os

def run_command(cmd):
    """执行命令并返回结果"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"错误: {result.stderr}")
    return result.stdout

def main():
    # 1. 启动浏览器
    print("步骤1: 启动浏览器")
    run_command("openclaw browser start")
    time.sleep(2)
    
    # 2. 打开搜索引擎
    print("步骤2: 打开百度")
    run_command("openclaw browser open https://baidu.com")
    time.sleep(3)
    
    # 3. 获取页面快照
    print("步骤3: 获取页面快照")
    snapshot = run_command("openclaw browser snapshot --json")
    
    try:
        snapshot_data = json.loads(snapshot)
        print(f"页面标题: {snapshot_data.get('title', '未知')}")
        print(f"找到 {len(snapshot_data.get('elements', []))} 个元素")
    except:
        print("快照数据:", snapshot[:200])
    
    # 4. 截图
    print("步骤4: 截图")
    screenshot_file = f"search_screenshot_{int(time.time())}.png"
    run_command(f"openclaw browser screenshot --full-page --output {screenshot_file}")
    
    if os.path.exists(screenshot_file):
        print(f"截图已保存: {screenshot_file}")
    else:
        print("截图失败")
    
    # 5. 关闭浏览器（可选）
    # run_command("openclaw browser stop")
    
    print("自动化完成")

if __name__ == "__main__":
    main()