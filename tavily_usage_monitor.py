#!/usr/bin/env python3
"""
Tavily 使用量监控
监控 API 使用情况，避免超出限制
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List
import os

class TavilyUsageMonitor:
    """Tavily 使用量监控类"""
    
    def __init__(self, usage_file: str = "tavily_usage_stats.json"):
        self.usage_file = usage_file
        self.usage_data = self.load_usage_data()
        
        # 免费版限制：每月1000次搜索
        self.monthly_limit = 1000
        self.daily_limit = 33  # 1000/30 ≈ 33次/天
        
    def load_usage_data(self) -> Dict:
        """加载使用数据"""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        
        # 初始化数据结构
        return {
            "monthly_usage": {
                "current_month": datetime.now().strftime("%Y-%m"),
                "total_searches": 0,
                "successful_searches": 0,
                "failed_searches": 0
            },
            "daily_usage": {},
            "hourly_usage": {},
            "alert_history": [],
            "rate_limits": {
                "monthly_limit": 1000,
                "daily_limit": 33,
                "hourly_limit": 50  # 保守估计
            }
        }
    
    def save_usage_data(self):
        """保存使用数据"""
        try:
            with open(self.usage_file, "w", encoding="utf-8") as f:
                json.dump(self.usage_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存使用数据失败: {e}")
    
    def record_search(self, success: bool = True, response_time: float = 0):
        """记录一次搜索"""
        now = datetime.now()
        month_key = now.strftime("%Y-%m")
        day_key = now.strftime("%Y-%m-%d")
        hour_key = now.strftime("%Y-%m-%d %H:00")
        
        # 更新月度数据
        if self.usage_data["monthly_usage"]["current_month"] != month_key:
            # 新月度，重置数据
            self.usage_data["monthly_usage"] = {
                "current_month": month_key,
                "total_searches": 0,
                "successful_searches": 0,
                "failed_searches": 0
            }
        
        self.usage_data["monthly_usage"]["total_searches"] += 1
        if success:
            self.usage_data["monthly_usage"]["successful_searches"] += 1
        else:
            self.usage_data["monthly_usage"]["failed_searches"] += 1
        
        # 更新每日数据
        if day_key not in self.usage_data["daily_usage"]:
            self.usage_data["daily_usage"][day_key] = {
                "total": 0,
                "successful": 0,
                "failed": 0,
                "avg_response_time": 0,
                "response_times": []
            }
        
        day_data = self.usage_data["daily_usage"][day_key]
        day_data["total"] += 1
        if success:
            day_data["successful"] += 1
        else:
            day_data["failed"] += 1
        
        # 记录响应时间
        if response_time > 0:
            day_data["response_times"].append(response_time)
            day_data["avg_response_time"] = sum(day_data["response_times"]) / len(day_data["response_times"])
        
        # 更新每小时数据
        if hour_key not in self.usage_data["hourly_usage"]:
            self.usage_data["hourly_usage"][hour_key] = 0
        self.usage_data["hourly_usage"][hour_key] += 1
        
        # 检查限制并保存
        self.check_limits()
        self.save_usage_data()
        
        return self.get_current_usage()
    
    def get_current_usage(self) -> Dict:
        """获取当前使用情况"""
        monthly = self.usage_data["monthly_usage"]
        day_key = datetime.now().strftime("%Y-%m-%d")
        daily = self.usage_data["daily_usage"].get(day_key, {"total": 0, "successful": 0, "failed": 0})
        
        # 计算使用率
        monthly_usage_rate = monthly["total_searches"] / self.monthly_limit
        daily_usage_rate = daily["total"] / self.daily_limit if self.daily_limit > 0 else 0
        
        return {
            "monthly": {
                "current": monthly["total_searches"],
                "limit": self.monthly_limit,
                "remaining": self.monthly_limit - monthly["total_searches"],
                "usage_rate": monthly_usage_rate,
                "success_rate": monthly["successful_searches"] / monthly["total_searches"] if monthly["total_searches"] > 0 else 0
            },
            "daily": {
                "current": daily["total"],
                "limit": self.daily_limit,
                "remaining": self.daily_limit - daily["total"],
                "usage_rate": daily_usage_rate,
                "success_rate": daily["successful"] / daily["total"] if daily["total"] > 0 else 0
            },
            "status": self.get_usage_status(monthly_usage_rate, daily_usage_rate)
        }
    
    def get_usage_status(self, monthly_rate: float, daily_rate: float) -> str:
        """获取使用状态"""
        if monthly_rate >= 1.0:
            return "CRITICAL"  # 超出月度限制
        elif monthly_rate >= 0.9:
            return "WARNING_HIGH"  # 接近月度限制
        elif monthly_rate >= 0.7:
            return "WARNING_MEDIUM"  # 使用量较高
        elif daily_rate >= 0.8:
            return "WARNING_DAILY_HIGH"  # 当日使用量高
        else:
            return "NORMAL"
    
    def check_limits(self):
        """检查限制并生成告警"""
        usage = self.get_current_usage()
        status = usage["status"]
        
        # 检查是否需要告警
        alerts = []
        
        if status == "CRITICAL":
            alerts.append({
                "level": "CRITICAL",
                "message": f"⚠️ 已超出月度限制！已使用 {usage['monthly']['current']}/{self.monthly_limit} 次搜索",
                "timestamp": datetime.now().isoformat()
            })
        elif status == "WARNING_HIGH":
            alerts.append({
                "level": "WARNING",
                "message": f"⚠️ 接近月度限制！已使用 {usage['monthly']['current']}/{self.monthly_limit} 次搜索 ({usage['monthly']['usage_rate']:.1%})",
                "timestamp": datetime.now().isoformat()
            })
        elif status == "WARNING_MEDIUM":
            alerts.append({
                "level": "INFO",
                "message": f"ℹ️ 使用量较高：{usage['monthly']['current']}/{self.monthly_limit} 次搜索 ({usage['monthly']['usage_rate']:.1%})",
                "timestamp": datetime.now().isoformat()
            })
        elif status == "WARNING_DAILY_HIGH":
            alerts.append({
                "level": "WARNING",
                "message": f"⚠️ 当日使用量高：{usage['daily']['current']}/{self.daily_limit} 次搜索",
                "timestamp": datetime.now().isoformat()
            })
        
        # 记录告警
        for alert in alerts:
            # 避免重复告警
            last_alerts = self.usage_data["alert_history"][-5:]  # 检查最近5条
            similar_alerts = [a for a in last_alerts if a.get("message", "").startswith(alert["message"][:50])]
            
            if not similar_alerts or (datetime.now() - datetime.fromisoformat(similar_alerts[-1]["timestamp"])).hours > 1:
                self.usage_data["alert_history"].append(alert)
    
    def get_usage_report(self, days: int = 7) -> Dict:
        """获取使用报告"""
        now = datetime.now()
        report = {
            "generated_at": now.isoformat(),
            "period_days": days,
            "summary": {},
            "daily_stats": [],
            "alerts": self.usage_data["alert_history"][-10:],  # 最近10条告警
            "recommendations": []
        }
        
        # 计算汇总统计
        monthly = self.usage_data["monthly_usage"]
        total_days = (now - datetime.strptime(monthly["current_month"] + "-01", "%Y-%m-%d")).days + 1
        
        report["summary"] = {
            "current_month": monthly["current_month"],
            "total_searches": monthly["total_searches"],
            "successful_searches": monthly["successful_searches"],
            "failed_searches": monthly["failed_searches"],
            "success_rate": monthly["successful_searches"] / monthly["total_searches"] if monthly["total_searches"] > 0 else 0,
            "avg_daily_searches": monthly["total_searches"] / total_days if total_days > 0 else 0,
            "monthly_limit_remaining": self.monthly_limit - monthly["total_searches"],
            "projected_monthly_usage": monthly["total_searches"] * 30 / total_days if total_days > 0 else 0
        }
        
        # 获取每日统计
        for i in range(days):
            date = now - timedelta(days=i)
            date_key = date.strftime("%Y-%m-%d")
            
            if date_key in self.usage_data["daily_usage"]:
                day_data = self.usage_data["daily_usage"][date_key]
                report["daily_stats"].append({
                    "date": date_key,
                    "total_searches": day_data["total"],
                    "successful": day_data["successful"],
                    "failed": day_data["failed"],
                    "success_rate": day_data["successful"] / day_data["total"] if day_data["total"] > 0 else 0,
                    "avg_response_time": day_data.get("avg_response_time", 0)
                })
        
        # 生成建议
        current_usage = self.get_current_usage()
        
        if current_usage["status"] == "CRITICAL":
            report["recommendations"].append("立即停止使用，等待下月重置或升级套餐")
        elif current_usage["status"] == "WARNING_HIGH":
            report["recommendations"].append("减少搜索频率，考虑缓存搜索结果")
        elif current_usage["status"] == "WARNING_MEDIUM":
            report["recommendations"].append("监控使用量，避免月底超限")
        
        if report["summary"]["projected_monthly_usage"] > self.monthly_limit:
            report["recommendations"].append(f"预计本月将使用 {report['summary']['projected_monthly_usage']:.0f} 次搜索，超出限制")
        
        return report
    
    def print_report(self, days: int = 7):
        """打印使用报告"""
        report = self.get_usage_report(days)
        
        print("Tavily API 使用量监控报告")
        print("=" * 60)
        print(f"生成时间: {report['generated_at']}")
        print(f"报告周期: 最近{days}天")
        print()
        
        # 月度汇总
        summary = report["summary"]
        print("月度汇总:")
        print(f"  当前月份: {summary['current_month']}")
        print(f"  总搜索次数: {summary['total_searches']}/{self.monthly_limit}")
        print(f"  成功搜索: {summary['successful_searches']} ({summary['success_rate']:.1%})")
        print(f"  失败搜索: {summary['failed_searches']}")
        print(f"  平均每日搜索: {summary['avg_daily_searches']:.1f}次")
        print(f"  剩余额度: {summary['monthly_limit_remaining']}次")
        print(f"  预计本月使用: {summary['projected_monthly_usage']:.0f}次")
        print()
        
        # 每日统计
        if report["daily_stats"]:
            print("每日统计:")
            for stat in report["daily_stats"]:
                print(f"  {stat['date']}: {stat['total_searches']}次搜索 "
                      f"({stat['success_rate']:.1%}成功率, "
                      f"响应{stat['avg_response_time']:.2f}秒)")
            print()
        
        # 告警
        if report["alerts"]:
            print("最近告警:")
            for alert in report["alerts"]:
                level_emoji = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🔵"}.get(alert.get("level", ""), "⚪")
                time_str = datetime.fromisoformat(alert["timestamp"]).strftime("%m-%d %H:%M")
                print(f"  {level_emoji} [{time_str}] {alert['message']}")
            print()
        
        # 建议
        if report["recommendations"]:
            print("建议:")
            for rec in report["recommendations"]:
                print(f"  • {rec}")
            print()
        
        # 当前状态
        current = self.get_current_usage()
        status_emoji = {
            "NORMAL": "✅",
            "WARNING_DAILY_HIGH": "⚠️",
            "WARNING_MEDIUM": "⚠️",
            "WARNING_HIGH": "🔴",
            "CRITICAL": "🛑"
        }.get(current["status"], "❓")
        
        print(f"当前状态: {status_emoji} {current['status']}")
        print(f"月度使用率: {current['monthly']['usage_rate']:.1%}")
        print(f"当日使用率: {current['daily']['usage_rate']:.1%}")

# 集成到 TavilyIntegration 的装饰器
def monitor_usage(func):
    """使用量监控装饰器"""
    def wrapper(self, *args, **kwargs):
        monitor = TavilyUsageMonitor()
        
        try:
            # 执行原函数
            result = func(self, *args, **kwargs)
            
            # 记录成功搜索
            response_time = result.get("response_time", 0) if isinstance(result, dict) else 0
            monitor.record_search(success=True, response_time=response_time)
            
            return result
        except Exception as e:
            # 记录失败搜索
            monitor.record_search(success=False)
            raise e
    
    return wrapper

if __name__ == "__main__":
    # 测试监控功能
    monitor = TavilyUsageMonitor()
    
    # 模拟一些搜索记录
    print("模拟记录搜索...")
    for i in range(5):
        success = i < 4  # 4次成功，1次失败
        response_time = 1.0 + i * 0.2
        monitor.record_search(success=success, response_time=response_time)
        time.sleep(0.1)
    
    # 显示报告
    print("\n" + "=" * 60)
    monitor.print_report(days=3)
    
    # 保存报告到文件
    report = monitor.get_usage_report(days=7)
    with open("tavily_usage_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细报告已保存到: tavily_usage_report.json")