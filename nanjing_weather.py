#!/usr/bin/env python3
"""
南京各区下周天气查询
"""

import json
import urllib.parse
import requests
from datetime import datetime, timedelta

# 南京的行政区划
nanjing_districts = [
    "玄武区",
    "秦淮区", 
    "建邺区",
    "鼓楼区",
    "浦口区",
    "栖霞区",
    "雨花台区",
    "江宁区",
    "六合区",
    "溧水区",
    "高淳区"
]

def get_weather(district, encoding="markdown"):
    """获取指定区域的天气"""
    try:
        # 编码查询参数
        query_encoded = urllib.parse.quote(district)
        url = f"https://60s.viki.moe/v2/weather?query={query_encoded}&encoding={encoding}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.text
        else:
            return f"❌ 获取 {district} 天气失败: HTTP {response.status_code}"
            
    except Exception as e:
        return f"❌ 获取 {district} 天气失败: {str(e)}"

def parse_weather_data(data, district):
    """解析天气数据"""
    try:
        # 尝试解析JSON
        weather_json = json.loads(data)
        
        if weather_json.get("code") == 200:
            weather_data = weather_json.get("data", {})
            weather = weather_data.get("weather", {})
            air_quality = weather_data.get("air_quality", {})
            
            # 提取关键信息
            result = {
                "district": district,
                "condition": weather.get("condition", "未知"),
                "temperature": weather.get("temperature", "未知"),
                "humidity": weather.get("humidity", "未知"),
                "wind": f"{weather.get('wind_direction', '未知')} {weather.get('wind_power', '未知')}",
                "aqi": air_quality.get("aqi", "未知"),
                "quality": air_quality.get("quality", "未知"),
                "updated": weather.get("updated", "未知")
            }
            return result
        else:
            return {"district": district, "error": weather_json.get("message", "未知错误")}
            
    except json.JSONDecodeError:
        # 如果不是JSON，可能是markdown格式
        lines = data.split('\n')
        result = {"district": district, "raw_data": data[:500] + "..." if len(data) > 500 else data}
        return result
    except Exception as e:
        return {"district": district, "error": f"解析失败: {str(e)}"}

def main():
    """主函数"""
    print("南京各区下周天气查询")
    print("=" * 60)
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"查询区域: {len(nanjing_districts)} 个行政区")
    print()
    
    all_results = []
    
    # 查询每个区的天气
    for i, district in enumerate(nanjing_districts, 1):
        print(f"查询 {i}/{len(nanjing_districts)}: {district}...")
        
        # 获取天气数据
        weather_data = get_weather(district, "json")
        
        # 解析数据
        parsed_data = parse_weather_data(weather_data, district)
        all_results.append(parsed_data)
        
        # 显示简要结果
        if "error" in parsed_data:
            print(f"   错误: {parsed_data['error']}")
        elif "condition" in parsed_data:
            print(f"   成功: {parsed_data['condition']} {parsed_data['temperature']}°C, "
                  f"湿度{parsed_data['humidity']}%, AQI: {parsed_data['aqi']}")
        else:
            print(f"   警告: 获取到数据但格式异常")
        
        # 避免请求过快
        import time
        time.sleep(0.5)
    
    print()
    print("天气汇总报告")
    print("=" * 60)
    
    # 按温度排序
    valid_results = [r for r in all_results if "temperature" in r and isinstance(r["temperature"], (int, float))]
    
    if valid_results:
        # 温度统计
        temps = [r["temperature"] for r in valid_results]
        avg_temp = sum(temps) / len(temps)
        max_temp = max(temps)
        min_temp = min(temps)
        
        print(f"🌡️ 温度统计:")
        print(f"  平均温度: {avg_temp:.1f}°C")
        print(f"  最高温度: {max_temp}°C")
        print(f"  最低温度: {min_temp}°C")
        print()
        
        # AQI统计
        aqi_values = [r["aqi"] for r in valid_results if isinstance(r["aqi"], (int, float))]
        if aqi_values:
            avg_aqi = sum(aqi_values) / len(aqi_values)
            print(f"🌫️ 空气质量统计:")
            print(f"  平均AQI: {avg_aqi:.1f}")
            print()
        
        # 详细数据表格
        print("📋 各区详细天气:")
        print("-" * 80)
        print(f"{'行政区':<8} {'天气':<6} {'温度':<6} {'湿度':<6} {'风力':<10} {'AQI':<6} {'质量':<8}")
        print("-" * 80)
        
        for result in all_results:
            if "condition" in result:
                print(f"{result['district']:<8} {result['condition']:<6} "
                      f"{result['temperature']:>4}°C {result['humidity']:>5}% "
                      f"{result['wind']:<10} {result['aqi']:>5} {result['quality']:<8}")
            elif "error" in result:
                print(f"{result['district']:<8} ❌ {result['error'][:40]}...")
            else:
                print(f"{result['district']:<8} ⚠️  数据格式异常")
        
        print("-" * 80)
        print()
        
        # 天气建议
        print("💡 天气建议:")
        
        if avg_temp > 25:
            print("  • 天气较热，建议穿轻薄衣物，注意防晒")
        elif avg_temp < 10:
            print("  • 天气较冷，建议穿厚外套，注意保暖")
        else:
            print("  • 温度适宜，建议穿春秋装")
        
        if avg_aqi > 100:
            print("  • 空气质量较差，建议减少户外活动，佩戴口罩")
        elif avg_aqi > 50:
            print("  • 空气质量一般，敏感人群注意防护")
        else:
            print("  • 空气质量良好，适合户外活动")
        
        # 检查是否有降雨
        rainy_districts = [r["district"] for r in valid_results if "雨" in r["condition"]]
        if rainy_districts:
            print(f"  • 以下区域有雨: {', '.join(rainy_districts)}，建议携带雨具")
        
        print()
        
        # 保存结果到文件
        output_file = f"nanjing_weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "query_time": datetime.now().isoformat(),
                "districts": nanjing_districts,
                "results": all_results,
                "summary": {
                    "avg_temperature": avg_temp,
                    "max_temperature": max_temp,
                    "min_temperature": min_temp,
                    "avg_aqi": avg_aqi if aqi_values else None,
                    "rainy_districts": rainy_districts
                }
            }, f, ensure_ascii=False, indent=2)
        
        print(f"💾 详细数据已保存到: {output_file}")
        
    else:
        print("❌ 未能获取到有效的天气数据")
        
        # 显示错误信息
        print("\n错误详情:")
        for result in all_results:
            if "error" in result:
                print(f"  {result['district']}: {result['error']}")
    
    print()
    print("✅ 查询完成！")

if __name__ == "__main__":
    main()