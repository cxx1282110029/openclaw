"""
修复版 Heartbeat 检查脚本
完全避免编码问题，适合Windows GBK环境
"""

import os
import subprocess
from datetime import datetime

def run_safe(cmd, timeout=10):
    """安全执行命令，避免编码问题"""
    try:
        # 使用二进制输出，避免编码问题
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            shell=True
        )
        # 尝试解码，如果失败则返回原始字节
        try:
            output = result.stdout.decode('gbk', errors='ignore')
        except:
            output = str(result.stdout)
        
        return output, result.returncode
    except Exception as e:
        return f"命令执行失败: {str(e)}", 1

def check_projects():
    """检查项目目录"""
    projects = [
        ("L_Intelligence", "E:\\L-Intelligence"),
        ("StockMonitor", "E:\\StockMonitor")
    ]
    
    alerts = []
    for name, path in projects:
        if os.path.exists(path):
            print(f"[OK] 项目目录存在: {name}")
        else:
            print(f"[ERROR] 项目目录缺失: {name}")
            alerts.append(f"项目目录缺失: {name}")
    
    return alerts

def check_memory_file():
    """检查今天的 memory 文件"""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_dir = os.path.join(os.path.dirname(__file__), "memory")
    memory_file = os.path.join(memory_dir, f"{today}.md")
    
    alerts = []
    if not os.path.exists(memory_file):
        os.makedirs(memory_dir, exist_ok=True)
        with open(memory_file, 'w', encoding='utf-8') as f:
            f.write(f"# {today}\n\n## Heartbeat 自动创建\n\n")
        print(f"[NOTE] 已自动创建今天的 memory 文件")
        alerts.append(f"已自动创建 memory 文件")
    else:
        print(f"[OK] 今天的 memory 文件已存在")
    
    return alerts

def check_gateway_status():
    """检查 Gateway 状态 - 简化检查"""
    alerts = []
    
    # 方法1: 直接检查端口
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('127.0.0.1', 18789))
        sock.close()
        
        if result == 0:
            print("[OK] Gateway 端口监听正常")
        else:
            print("[WARN] Gateway 端口未监听")
            alerts.append("Gateway 端口未监听")
    except:
        pass
    
    # 方法2: 尝试执行命令（忽略输出编码）
    output, code = run_safe("openclaw gateway status", timeout=5)
    if code == 0:
        print("[OK] Gateway 命令执行成功")
    else:
        print("[ERROR] Gateway 命令执行失败")
        alerts.append("Gateway 检查失败")
    
    return alerts

def check_git_status():
    """检查 Git 状态"""
    alerts = []
    
    # 切换到工作目录
    workspace = os.path.dirname(__file__)
    os.chdir(workspace)
    
    # 检查是否有未提交文件
    output, code = run_safe("git status")
    if code == 0:
        if "nothing to commit" in output or "无文件要提交" in output:
            print("[OK] Git 工作区干净")
        else:
            print("[WARN] Git 有未提交文件")
            alerts.append("Git 有未提交文件")
    else:
        print("[ERROR] Git 检查失败")
    
    return alerts

def main():
    """主函数"""
    # 设置控制台编码为UTF-8（Windows下）
    try:
        import sys
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass
    
    print(f"Heartbeat 检查开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    all_alerts = []
    
    # 执行所有检查
    all_alerts.extend(check_projects())
    all_alerts.extend(check_memory_file())
    all_alerts.extend(check_gateway_status())
    all_alerts.extend(check_git_status())
    
    print("=" * 50)
    
    if len(all_alerts) == 0:
        print(f"[OK] 检查完成，所有系统正常")
        # 正常情况：返回0（标准Unix约定）
        return_code = 0
    else:
        print(f"[WARN] 检查完成，发现 {len(all_alerts)} 个问题")
        # 发现问题：返回1（标准Unix约定）
        return_code = 1
    
    if all_alerts:
        print("\n需要关注的问题:")
        for i, alert in enumerate(all_alerts, 1):
            print(f"  {i}. {alert}")
    
    # 标准逻辑：正常为0，有问题为1（Unix退出码约定）
    return return_code

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)