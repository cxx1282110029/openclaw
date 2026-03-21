#!/usr/bin/env python3
# 快速磁盘检查

import shutil
from datetime import datetime

def main():
    print("C盘快速检查")
    print("=" * 40)
    
    try:
        # 检查C盘空间
        total, used, free = shutil.disk_usage("C:/")
        
        # 转换为GB
        total_gb = total / (1024**3)
        used_gb = used / (1024**3)
        free_gb = free / (1024**3)
        
        # 计算百分比
        used_percent = (used / total) * 100
        
        print(f"总容量: {total_gb:.1f} GB")
        print(f"已使用: {used_gb:.1f} GB ({used_percent:.1f}%)")
        print(f"可用空间: {free_gb:.1f} GB")
        print()
        
        # 状态评估
        print("状态评估:")
        if free_gb > 50:
            print("  安全 - 可用空间充足 (>50GB)")
            status = "安全"
        elif free_gb > 20:
            print("  警告 - 空间开始紧张 (20-50GB)")
            status = "警告"
        else:
            print("  危险 - 空间严重不足 (<20GB)")
            status = "危险"
        
        print()
        print("建议:")
        if free_gb > 50:
            print("  1. 保持定期维护即可")
            print("  2. 每月清理临时文件")
            print("  3. 每季度整理下载文件夹")
        elif free_gb > 20:
            print("  1. 建议近期清理")
            print("  2. 清理临时文件")
            print("  3. 清空回收站")
            print("  4. 检查下载文件夹")
        else:
            print("  1. 需要立即清理")
            print("  2. 运行磁盘清理工具")
            print("  3. 移动大文件到其他盘")
            print("  4. 考虑扩容")
        
        # 保存记录
        with open("memory/disk_check.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | ")
            f.write(f"总:{total_gb:.1f}GB 已用:{used_gb:.1f}GB 可用:{free_gb:.1f}GB 状态:{status}\n")
        
        print()
        print(f"检查完成: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
    except Exception as e:
        print(f"检查失败: {e}")

if __name__ == "__main__":
    main()