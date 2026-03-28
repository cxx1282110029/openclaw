#!/usr/bin/env python3
"""
南京主要区域天气查询 - 简化版
"""

import urllib.parse
import requests

# 南京主要区域
main_districts = [
    "玄武区",
    "秦淮区", 
    "建邺区",
    "鼓楼区",
    "江宁区",
    "浦口区"
]

def get_simple_weather(district):
    """获取简化天气信息"""
    try:
        query_encoded = urllib.parse.quote(district)
        url = f"https://60s.viki.moe/v2/weather?query={query_encoded}&encoding=json"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                weather_data = data.get("data", {})
                weather = weather_data.get("weather", {})
                air_quality = weather_data.get("air_quality", {})
                
                return {
                    "district": district,
                    "condition": weather.get("condition", "未知"),
                    "temperature": weather.get("temperature", "未知"),
                    "humidity": weather.get("humidity", "未知"),
                    "wind": f"{weather.get('wind_direction', '未知')} {weather.get('wind_power', '未知')}",
                    "aqi": air_quality.get("aqi", "未知"),
                    "quality": air_quality.get("quality", "未知")
                }
            else:
                return {"district": district, "error": data.get("message", "API错误")}
        else:
            return {"district": district, "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"district": district, "error": str(e)}

def main():
    """主函数"""
    print("南京主要区域天气查询")
    print("=" * 50)
    print("查询时间: 2026-03-28 19:58")
    print()
    
    results = []
    
    # 查询每个区域
    for district in main_districts:
        print(f"查询: {district}")
        result = get_simple_weather(district)
        results.append(result)
        
        if "error" in result:
            print(f"  错误: {result['error']}")
        else:
            print(f"  天气: {result['condition']}")
            print(f"  温度: {result['temperature']}°C")
            print(f"  湿度: {result['humidity']}%")
            print(f"  风力: {result['wind']}")
            print(f"  空气质量: AQI {result['aqi']} ({result['quality']})")
        print()
    
    # 汇总统计
    print("天气汇总")
    print("=" * 50)
    
    valid_results = [r for r in results if "temperature" in r and isinstance(r["temperature"], (int, float))]
    
    if valid_results:
        temps = [r["temperature"] for r in valid_results]
        avg_temp = sum(temps) / len(temps)
        max_temp = max(temps)
        min_temp = min(temps)
        
        print(f"温度统计:")
        print(f"  平均: {avg_temp:.1f}°C")
        print(f"  最高: {max_temp}°C")
        print(f"  最低: {min_temp}°C")
        print()
        
        # 显示表格
        print("详细数据:")
        print("-" * 70)
        print(f"{'区域':<6} {'天气':<6} {'温度':<6} {'湿度':<6} {'风力':<10} {'AQI':<6} {'质量':<8}")
        print("-" * 70)
        
        for result in results:
            if "temperature" in result:
                print(f"{result['district']:<6} {result['condition']:<6} "
                      f"{result['temperature']:>4}°C {result['humidity']:>5}% "
                      f"{result['wind']:<10} {result['aqi']:>5} {result['quality']:<8}")
            else:
                print(f"{result['district']:<6} 错误: {result.get('error', '未知')[:30]}")
        
        print("-" * 70)
        print()
        
        # 建议
        print("建议:")
        if avg_temp > 20:
            print("  • 天气温暖，适合户外活动")
        elif avg_temp > 10:
            print("  • 天气凉爽，建议穿外套")
        else:
            print("  • 天气较冷，注意保暖")
        
        # 检查是否有雨
        rainy = [r["district"] for r in valid_results if "雨" in r["condition"]]
        if rainy:
            print(f"  • {', '.join(rainy)} 有雨，建议带伞")
        
        print()
        print("查询完成！")

if __name__ == "__main__":
    main()