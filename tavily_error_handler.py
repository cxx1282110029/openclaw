#!/usr/bin/env python3
"""
Tavily 错误处理模块
处理 API 错误、重试机制和故障恢复
"""

import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable, Any
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tavily_errors.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TavilyErrorHandler')

class TavilyErrorHandler:
    """Tavily 错误处理类"""
    
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.error_stats = self.load_error_stats()
        
        # 错误类型定义
        self.error_types = {
            "network": ["ConnectionError", "Timeout", "ConnectTimeout"],
            "api": ["HTTP 4xx", "HTTP 5xx", "Invalid API Key", "Rate Limit"],
            "data": ["JSON Parse Error", "Invalid Response Format"],
            "system": ["Memory Error", "Disk Error", "Unknown Error"]
        }
    
    def load_error_stats(self) -> Dict:
        """加载错误统计"""
        try:
            with open("tavily_error_stats.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {
                "total_errors": 0,
                "error_by_type": {},
                "error_by_hour": {},
                "recovery_attempts": 0,
                "successful_recoveries": 0,
                "last_error": None,
                "error_history": []
            }
    
    def save_error_stats(self):
        """保存错误统计"""
        try:
            with open("tavily_error_stats.json", "w", encoding="utf-8") as f:
                json.dump(self.error_stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存错误统计失败: {e}")
    
    def classify_error(self, error: Exception) -> str:
        """分类错误类型"""
        error_str = str(error)
        
        # 网络错误
        if any(net_err in error_str for net_err in ["Connection", "Timeout", "Network"]):
            return "network"
        
        # API 错误
        elif any(api_err in error_str for api_err in ["HTTP", "API", "Key", "Rate", "Limit"]):
            return "api"
        
        # 数据错误
        elif any(data_err in error_str for data_err in ["JSON", "Parse", "Format", "Invalid"]):
            return "data"
        
        # 系统错误
        else:
            return "system"
    
    def record_error(self, error: Exception, context: Dict = None):
        """记录错误"""
        error_type = self.classify_error(error)
        error_time = datetime.now()
        hour_key = error_time.strftime("%Y-%m-%d %H:00")
        
        # 更新统计
        self.error_stats["total_errors"] += 1
        
        # 按类型统计
        if error_type not in self.error_stats["error_by_type"]:
            self.error_stats["error_by_type"][error_type] = 0
        self.error_stats["error_by_type"][error_type] += 1
        
        # 按小时统计
        if hour_key not in self.error_stats["error_by_hour"]:
            self.error_stats["error_by_hour"][hour_key] = 0
        self.error_stats["error_by_hour"][hour_key] += 1
        
        # 记录错误详情
        error_record = {
            "timestamp": error_time.isoformat(),
            "type": error_type,
            "error": str(error),
            "context": context or {},
            "resolved": False
        }
        
        self.error_stats["error_history"].append(error_record)
        self.error_stats["last_error"] = error_record
        
        # 只保留最近100条错误记录
        if len(self.error_stats["error_history"]) > 100:
            self.error_stats["error_history"] = self.error_stats["error_history"][-100:]
        
        # 保存统计
        self.save_error_stats()
        
        # 记录日志
        logger.error(f"错误类型: {error_type}, 错误信息: {error}, 上下文: {context}")
        
        return error_record
    
    def retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """带退避的重试机制"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                result = func(*args, **kwargs)
                
                # 如果之前有错误，记录恢复成功
                if last_error:
                    self.record_recovery(last_error)
                
                return result
                
            except Exception as e:
                last_error = e
                
                # 记录错误
                error_record = self.record_error(e, {
                    "function": func.__name__,
                    "attempt": attempt + 1,
                    "max_retries": self.max_retries
                })
                
                # 如果是最后一次尝试，抛出异常
                if attempt == self.max_retries - 1:
                    logger.error(f"达到最大重试次数 ({self.max_retries})，放弃重试")
                    raise
                
                # 计算退避延迟
                delay = self.retry_delay * (2 ** attempt)  # 指数退避
                logger.warning(f"第 {attempt + 1} 次尝试失败，{delay:.1f}秒后重试...")
                
                # 等待
                time.sleep(delay)
    
    def record_recovery(self, error: Exception):
        """记录恢复成功"""
        self.error_stats["recovery_attempts"] += 1
        self.error_stats["successful_recoveries"] += 1
        
        # 标记错误为已解决
        if self.error_stats["error_history"]:
            last_error = self.error_stats["error_history"][-1]
            last_error["resolved"] = True
            last_error["resolved_at"] = datetime.now().isoformat()
        
        self.save_error_stats()
        logger.info(f"错误恢复成功: {error}")
    
    def get_error_report(self) -> Dict:
        """获取错误报告"""
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        # 计算错误率
        total_errors = self.error_stats["total_errors"]
        recovery_rate = (
            self.error_stats["successful_recoveries"] / 
            self.error_stats["recovery_attempts"] 
            if self.error_stats["recovery_attempts"] > 0 else 0
        )
        
        # 最近错误
        recent_errors = [
            err for err in self.error_stats["error_history"]
            if datetime.fromisoformat(err["timestamp"]) > hour_ago
        ]
        
        return {
            "generated_at": now.isoformat(),
            "summary": {
                "total_errors": total_errors,
                "recovery_attempts": self.error_stats["recovery_attempts"],
                "successful_recoveries": self.error_stats["successful_recoveries"],
                "recovery_rate": recovery_rate,
                "errors_last_hour": len(recent_errors),
                "errors_last_24h": len([
                    err for err in self.error_stats["error_history"]
                    if datetime.fromisoformat(err["timestamp"]) > day_ago
                ])
            },
            "error_distribution": self.error_stats["error_by_type"],
            "recent_errors": recent_errors[-10:],  # 最近10条错误
            "health_status": self.get_health_status(len(recent_errors)),
            "recommendations": self.get_recommendations()
        }
    
    def get_health_status(self, recent_error_count: int) -> str:
        """获取健康状态"""
        if recent_error_count == 0:
            return "HEALTHY"
        elif recent_error_count <= 3:
            return "STABLE"
        elif recent_error_count <= 10:
            return "DEGRADED"
        else:
            return "CRITICAL"
    
    def get_recommendations(self) -> list:
        """获取建议"""
        recommendations = []
        error_dist = self.error_stats["error_by_type"]
        
        # 基于错误类型的建议
        if error_dist.get("network", 0) > 5:
            recommendations.append("网络错误较多，检查网络连接和代理设置")
        
        if error_dist.get("api", 0) > 3:
            recommendations.append("API错误较多，检查API密钥和配额")
        
        if error_dist.get("rate_limit", 0) > 0:
            recommendations.append("检测到速率限制，减少请求频率或升级套餐")
        
        # 基于错误频率的建议
        recent_errors = [
            err for err in self.error_stats["error_history"]
            if datetime.fromisoformat(err["timestamp"]) > datetime.now() - timedelta(hours=1)
        ]
        
        if len(recent_errors) > 5:
            recommendations.append("最近错误频繁，考虑暂停服务并检查系统")
        
        return recommendations
    
    def handle_api_error(self, response: requests.Response) -> Dict:
        """处理API响应错误"""
        try:
            error_data = response.json()
        except:
            error_data = {"error": response.text[:200]}
        
        error_msg = f"HTTP {response.status_code}: {error_data}"
        
        # 特殊处理常见错误
        if response.status_code == 401:
            error_msg = "API密钥无效或过期"
        elif response.status_code == 429:
            error_msg = "达到速率限制，请稍后重试"
        elif response.status_code >= 500:
            error_msg = "服务器内部错误，可能是Tavily服务问题"
        
        # 记录错误
        self.record_error(Exception(error_msg), {
            "status_code": response.status_code,
            "response": error_data,
            "url": response.url
        })
        
        return {
            "error": error_msg,
            "status_code": response.status_code,
            "details": error_data
        }
    
    def create_fallback_response(self, original_query: str) -> Dict:
        """创建降级响应"""
        logger.warning(f"为查询 '{original_query}' 创建降级响应")
        
        # 简单的降级逻辑
        fallback_data = {
            "query": original_query,
            "answer": f"由于系统暂时不可用，无法获取'{original_query}'的最新信息。",
            "results": [],
            "response_time": 0,
            "fallback": True,
            "fallback_reason": "API服务暂时不可用",
            "suggestions": [
                "稍后重试",
                "检查网络连接",
                "验证API密钥"
            ]
        }
        
        return fallback_data
    
    def print_error_report(self):
        """打印错误报告"""
        report = self.get_error_report()
        
        print("Tavily 错误处理报告")
        print("=" * 60)
        print(f"生成时间: {report['generated_at']}")
        print()
        
        # 摘要
        summary = report["summary"]
        print("错误摘要:")
        print(f"  总错误数: {summary['total_errors']}")
        print(f"  恢复尝试: {summary['recovery_attempts']}")
        print(f"  成功恢复: {summary['successful_recoveries']}")
        print(f"  恢复率: {summary['recovery_rate']:.1%}")
        print(f"  最近1小时错误: {summary['errors_last_hour']}")
        print(f"  最近24小时错误: {summary['errors_last_24h']}")
        print()
        
        # 错误分布
        if report["error_distribution"]:
            print("错误分布:")
            for error_type, count in report["error_distribution"].items():
                print(f"  {error_type}: {count}次")
            print()
        
        # 健康状态
        status_emoji = {
            "HEALTHY": "✅",
            "STABLE": "🟡",
            "DEGRADED": "🟠",
            "CRITICAL": "🔴"
        }.get(report["health_status"], "❓")
        
        print(f"健康状态: {status_emoji} {report['health_status']}")
        print()
        
        # 最近错误
        if report["recent_errors"]:
            print("最近错误:")
            for error in report["recent_errors"][-5:]:  # 最近5条
                time_str = datetime.fromisoformat(error["timestamp"]).strftime("%H:%M")
                resolved = "✅" if error.get("resolved", False) else "❌"
                print(f"  [{time_str}] {resolved} {error['type']}: {error['error'][:50]}...")
            print()
        
        # 建议
        if report["recommendations"]:
            print("建议:")
            for rec in report["recommendations"]:
                print(f"  • {rec}")
            print()

# 使用示例
def test_error_handling():
    """测试错误处理"""
    handler = TavilyErrorHandler(max_retries=2)
    
    print("测试错误处理功能...")
    
    # 测试1: 记录一些错误
    print("\n1. 记录测试错误:")
    try:
        raise ConnectionError("测试网络连接错误")
    except Exception as e:
        handler.record_error(e, {"test": True})
    
    try:
        raise ValueError("测试数据格式错误")
    except Exception as e:
        handler.record_error(e, {"test": True})
    
    # 测试2: 重试机制
    print("\n2. 测试重试机制:")
    
    def failing_function(attempts_to_fail: int = 2):
        """模拟失败函数"""
        if not hasattr(failing_function, "call_count"):
            failing_function.call_count = 0
        
        failing_function.call_count += 1
        
        if failing_function.call_count <= attempts_to_fail:
            raise ConnectionError(f"模拟失败 (第{failing_function.call_count}次)")
        
        return "成功!"
    
    try:
        result = handler.retry_with_backoff(failing_function, attempts_to_fail=2)
        print(f"重试结果: {result}")
    except Exception as e:
        print(f"重试失败: {e}")
    
    # 测试3: 显示报告
    print("\n3. 错误报告:")
    handler.print_error_report()
    
    # 保存报告
    report = handler.get_error_report()
    with open("tavily_error_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细报告已保存到: tavily_error_report.json")

if __name__ == "__main__":
    test_error_handling()