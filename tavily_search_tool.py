#!/usr/bin/env python3
"""
Tavily 搜索工具
用户友好的命令行搜索工具
"""

import sys
import json
import argparse
from datetime import datetime
from tavily_integration import TavilyIntegration

class TavilySearchTool:
    """Tavily 搜索工具类"""
    
    def __init__(self):
        self.tavily = TavilyIntegration()
        self.setup_argparse()
    
    def setup_argparse(self):
        """设置命令行参数解析"""
        self.parser = argparse.ArgumentParser(
            description="Tavily AI 搜索工具",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
使用示例:
  %(prog)s "人工智能最新发展"                    # 基本搜索
  %(prog)s "OpenAI" --max-results 5             # 指定结果数量
  %(prog)s "科技新闻" --time-range day          # 今日新闻
  %(prog)s --batch-file queries.txt            # 批量搜索
  %(prog)s --stats                             # 查看使用统计
  %(prog)s --monitor "区块链" --interval 6      # 监控主题
            """
        )
        
        # 搜索参数
        self.parser.add_argument("query", nargs="?", help="搜索关键词")
        self.parser.add_argument("--max-results", type=int, default=3, help="最大结果数 (默认: 3)")
        self.parser.add_argument("--time-range", choices=["day", "week", "month", "year"], 
                                help="时间范围: day(今天), week(本周), month(本月), year(今年)")
        self.parser.add_argument("--include-answer", action="store_true", default=True,
                                help="包含AI答案 (默认: 是)")
        self.parser.add_argument("--no-answer", action="store_false", dest="include_answer",
                                help="不包含AI答案")
        
        # 批量操作
        self.parser.add_argument("--batch-file", help="批量搜索文件 (每行一个查询)")
        self.parser.add_argument("--output", help="输出文件 (JSON格式)")
        
        # 工具功能
        self.parser.add_argument("--stats", action="store_true", help="显示使用统计")
        self.parser.add_argument("--history", action="store_true", help="显示搜索历史")
        self.parser.add_argument("--monitor", help="监控特定主题")
        self.parser.add_argument("--interval", type=int, default=24, 
                                help="监控间隔(小时) (默认: 24)")
        self.parser.add_argument("--export-history", help="导出搜索历史到文件")
    
    def print_results(self, results: dict, query: str = ""):
        """格式化打印搜索结果"""
        if "error" in results:
            print(f"搜索错误: {results['error']}")
            if "response_text" in results:
                print(f"响应: {results['response_text']}")
            return
        
        print(f"\n搜索: {query or results.get('query', '未知')}")
        print(f"响应时间: {results.get('response_time', 0):.2f}秒")
        print("-" * 60)
        
        # AI 答案
        if "answer" in results and results["answer"]:
            print(f"AI 答案:\n  {results['answer']}\n")
        
        # 搜索结果
        if "results" in results and results["results"]:
            print(f"找到 {len(results['results'])} 个结果:")
            for i, result in enumerate(results["results"], 1):
                print(f"\n{i}. {result.get('title', '无标题')}")
                print(f"   链接: {result.get('url', '无URL')}")
                content = result.get('content', '无内容')
                if len(content) > 200:
                    content = content[:200] + "..."
                print(f"   摘要: {content}")
                if "score" in result:
                    print(f"   相关性: {result['score']:.1%}")
        
        # 相关问题
        if "follow_up_questions" in results and results["follow_up_questions"]:
            print(f"\n相关问题:")
            for q in results["follow_up_questions"][:3]:
                print(f"  • {q}")
    
    def search(self, args):
        """执行搜索"""
        if args.batch_file:
            self.batch_search(args)
        else:
            self.single_search(args)
    
    def single_search(self, args):
        """单次搜索"""
        if not args.query:
            print("错误: 需要搜索关键词")
            self.parser.print_help()
            return
        
        print(f"正在搜索: {args.query}")
        
        # 构建搜索参数
        search_kwargs = {
            "max_results": args.max_results,
            "include_answer": args.include_answer
        }
        
        if args.time_range:
            search_kwargs["time_range"] = args.time_range
        
        # 执行搜索
        results = self.tavily.search(args.query, **search_kwargs)
        
        # 显示结果
        self.print_results(results, args.query)
        
        # 保存结果
        if args.output:
            self.save_results(results, args.output)
            print(f"\n结果已保存到: {args.output}")
    
    def batch_search(self, args):
        """批量搜索"""
        try:
            with open(args.batch_file, "r", encoding="utf-8") as f:
                queries = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"错误: 文件不存在 - {args.batch_file}")
            return
        
        print(f"批量搜索 {len(queries)} 个查询...")
        
        all_results = []
        for query in queries:
            print(f"\n搜索: {query}")
            results = self.tavily.search(query, max_results=args.max_results)
            
            if "error" not in results:
                all_results.append({
                    "query": query,
                    "results": results.get("results", []),
                    "answer": results.get("answer", ""),
                    "response_time": results.get("response_time", 0)
                })
            
            # 显示简要结果
            if "results" in results:
                print(f"  找到 {len(results['results'])} 个结果")
        
        # 保存批量结果
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(all_results, f, ensure_ascii=False, indent=2)
            print(f"\n批量结果已保存到: {args.output}")
    
    def save_results(self, results: dict, filename: str):
        """保存结果到文件"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    
    def show_stats(self):
        """显示使用统计"""
        stats = self.tavily.get_usage_stats()
        
        print("Tavily Search 使用统计")
        print("=" * 40)
        print(f"总搜索次数: {stats.get('total_searches', 0)}")
        print(f"成功搜索: {stats.get('successful_searches', 0)}")
        print(f"成功率: {stats.get('success_rate', 0):.1%}")
        print(f"平均响应时间: {stats.get('avg_response_time', 0):.2f}秒")
        
        if stats['last_search']:
            last_time = datetime.fromisoformat(stats['last_search'].replace('Z', '+00:00'))
            print(f"最后搜索: {last_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def show_history(self):
        """显示搜索历史"""
        if not self.tavily.search_history:
            print("暂无搜索历史")
            return
        
        print("搜索历史")
        print("=" * 40)
        
        for i, record in enumerate(self.tavily.search_history[-10:], 1):  # 显示最近10条
            time_str = datetime.fromisoformat(record['timestamp']).strftime('%m-%d %H:%M')
            status = "成功" if record.get('success', False) else "失败"
            
            print(f"{i}. [{time_str}] {record['query']}")
            print(f"   状态: {status}")
            
            if record.get('success', False):
                print(f"   结果数: {record.get('results_count', 0)}")
                print(f"   响应时间: {record.get('response_time', 0):.2f}秒")
            else:
                print(f"   错误: {record.get('error', '未知错误')}")
            print()
    
    def export_history(self, filename: str):
        """导出搜索历史"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.tavily.search_history, f, ensure_ascii=False, indent=2)
            print(f"搜索历史已导出到: {filename}")
        except Exception as e:
            print(f"导出失败: {e}")
    
    def monitor_topic(self, topic: str, interval_hours: int):
        """监控主题"""
        from tavily_integration import integrate_with_automation
        
        integration = integrate_with_automation()
        result = integration["monitor_topic"](topic, interval_hours)
        
        if result:
            print(f"\n监控结果 - {topic}")
            print(f"监控时间: {result['monitor_time']}")
            print(f"发现新文章: {result['new_articles']}篇")
            
            for i, article in enumerate(result['latest_articles'], 1):
                print(f"\n{i}. {article['title']}")
                print(f"   链接: {article['url']}")
                print(f"   摘要: {article['summary']}")
                print(f"   发布时间: {article['published']}")
        else:
            print(f"监控失败: {topic}")
    
    def run(self):
        """运行工具"""
        args = self.parser.parse_args()
        
        # 执行相应功能
        if args.stats:
            self.show_stats()
        elif args.history:
            self.show_history()
        elif args.export_history:
            self.export_history(args.export_history)
        elif args.monitor:
            self.monitor_topic(args.monitor, args.interval)
        elif args.query or args.batch_file:
            self.search(args)
        else:
            self.parser.print_help()

def main():
    """主函数"""
    tool = TavilySearchTool()
    tool.run()

if __name__ == "__main__":
    main()