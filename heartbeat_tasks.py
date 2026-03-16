"""
Heartbeat 自动化任务脚本
被 HEARTBEAT.md 触发执行
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
STATE_FILE = Path(__file__).parent / "memory" / "heartbeat-state.json"
PROJECTS = {
    "L_Intelligence": "E:\\L-Intelligence",
    "StockMonitor": "E:\\StockMonitor"
}

class HeartbeatChecker:
    def __init__(self):
        self.state = self._load_state()
        self.alerts = []
        
    def _load_state(self) -> dict:
        """加载状态文件"""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "lastCheck": None,
            "projectStatus": {},
            "alertHistory": []
        }
    
    def _save_state(self):
        """保存状态"""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def _should_alert(self, key: str, cooldown_hours: int = 2) -> bool:
        """检查是否应该发送告警[CHAR]避免重复[CHAR]"""
        now = datetime.now()
        last_alert = self.state.get("alertHistory", {}).get(key)
        
        if not last_alert:
            return True
        
        last_time = datetime.fromisoformat(last_alert)
        hours_since = (now - last_time).total_seconds() / 3600
        
        return hours_since >= cooldown_hours
    
    def _record_alert(self, key: str):
        """记录告警时间"""
        if "alertHistory" not in self.state:
            self.state["alertHistory"] = {}
        self.state["alertHistory"][key] = datetime.now().isoformat()
    
    def check_projects(self):
        """检查项目状态"""
        for name, path in PROJECTS.items():
            if not os.path.exists(path):
                msg = f"[CHAR][CHAR] 项目 `{name}` 路径不存在: {path}"
                if self._should_alert(f"missing_{name}"):
                    self.alerts.append(msg)
                    self._record_alert(f"missing_{name}")
                continue
            
            # 检查是否有错误日志
            log_files = [
                os.path.join(path, "error.log"),
                os.path.join(path, "app.log"),
                os.path.join(path, "logs", "app.log")
            ]
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    # 检查最近1小时是否有错误
                    mtime = datetime.fromtimestamp(os.path.getmtime(log_file))
                    hours_ago = (datetime.now() - mtime).total_seconds() / 3600
                    
                    if hours_ago < 1:  # 最近1小时有更新
                        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            recent_lines = lines[-50:]  # 最后50行
                            
                            for line in recent_lines:
                                if 'error' in line.lower() or 'exception' in line.lower():
                                    msg = f"[CHAR][CHAR] `{name}` 最近有错误日志:\n```\n{line[:100]}...\n```"
                                    if self._should_alert(f"error_{name}", cooldown_hours=1):
                                        self.alerts.append(msg)
                                        self._record_alert(f"error_{name}")
                                    break
    
    def check_memory_file(self):
        """检查今天的 memory 文件"""
        today = datetime.now().strftime("%Y-%m-%d")
        memory_file = Path(__file__).parent / "memory" / f"{today}.md"
        
        if not memory_file.exists():
            # 自动创建今天的 memory 文件
            memory_file.parent.mkdir(parents=True, exist_ok=True)
            with open(memory_file, 'w', encoding='utf-8') as f:
                f.write(f"# {today}\n\n## Heartbeat 自动创建\n\n")
            self.alerts.append(f"[NOTE] 已自动创建今天的 memory 文件: {today}.md")
    
    def check_gateway_status(self):
        """检查 Gateway 状态"""
        try:
            result = subprocess.run(
                ["openclaw", "gateway", "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if "running" not in result.stdout.lower():
                msg = f"[CHAR][CHAR] Gateway 状态异常[CHAR]可能需要重启\n```\n{result.stdout}\n```"
                if self._should_alert("gateway_down"):
                    self.alerts.append(msg)
                    self._record_alert("gateway_down")
        except Exception as e:
            msg = f"[CHAR][CHAR] 检查 Gateway 状态失败: {e}"
            if self._should_alert("gateway_check_failed"):
                self.alerts.append(msg)
                self._record_alert("gateway_check_failed")
    
    def check_git_status(self):
        """检查 workspace git 状态"""
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=Path(__file__).parent,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout.strip():
                files = len(result.stdout.strip().split('\n'))
                if files > 5 and self._should_alert("git_uncommitted", cooldown_hours=4):
                    self.alerts.append(f"[GIT] Workspace 有 {files} 个未提交文件[CHAR]建议执行 git commit")
                    self._record_alert("git_uncommitted")
        except Exception:
            pass  # git 检查失败不告警
    
    def run_all_checks(self) -> list:
        """运行所有检查"""
        print(f"Heartbeat 检查开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.check_projects()
        self.check_memory_file()
        self.check_gateway_status()
        self.check_git_status()
        
        # 更新检查时间
        self.state["lastCheck"] = datetime.now().isoformat()
        self._save_state()
        
        print(f"[OK] 检查完成[CHAR]发现 {len(self.alerts)} 个问题")
        
        return self.alerts


if __name__ == "__main__":
    checker = HeartbeatChecker()
    alerts = checker.run_all_checks()
    
    if alerts:
        print("\n[CHAR] 需要通知的告警:")
        for alert in alerts:
            print(f"  - {alert[:100]}...")
    else:
        print("\n[CHAR] 一切正常[CHAR]无需通知")
