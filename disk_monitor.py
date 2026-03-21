#!/usr/bin/env python3
# C盘容量监控脚本

import os
import shutil
import json
from datetime import datetime

def check_disk_space():
    """检查磁盘空间"""
    
    print("C盘容量检查报告")
    print("=" * 50)
    
    # 检查C盘空间
    try:
        total, used, free = shutil.disk_usage("C:/")
        
        # 转换为GB
        total_gb = total / (1024**3)
        used_gb = used / (1024**3)
        free_gb = free / (1024**3)
        
        # 计算百分比
        used_percent = (used / total) * 100
        free_percent = (free / total) * 100
        
        print(f"总容量: {total_gb:.2f} GB")
        print(f"已使用: {used_gb:.2f} GB ({used_percent:.1f}%)")
        print(f"可用空间: {free_gb:.2f} GB ({free_percent:.1f}%)")
        
        # 状态评估
        print("\n状态评估:")
        if free_gb > 50:
            print("  状态: 安全 (可用空间 > 50GB)")
            status = "safe"
        elif free_gb > 20:
            print("  状态: 警告 (可用空间 20-50GB)")
            status = "warning"
        else:
            print("  状态: 危险 (可用空间 < 20GB)")
            status = "danger"
        
        # 检查大目录
        print("\n大目录检查:")
        large_dirs = check_large_directories("C:/", limit_mb=100)
        
        for dir_info in large_dirs[:10]:  # 显示前10个
            print(f"  - {dir_info['path']}: {dir_info['size_mb']:.1f} MB")
        
        # 保存检查记录
        save_check_record({
            'timestamp': datetime.now().isoformat(),
            'total_gb': total_gb,
            'used_gb': used_gb,
            'free_gb': free_gb,
            'used_percent': used_percent,
            'status': status,
            'large_dirs': large_dirs[:5]
        })
        
        return {
            'total_gb': total_gb,
            'used_gb': used_gb,
            'free_gb': free_gb,
            'status': status
        }
        
    except Exception as e:
        print(f"检查失败: {e}")
        return None

def check_large_directories(path, limit_mb=100):
    """检查大目录"""
    large_dirs = []
    
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            
            # 跳过无权限访问的目录
            try:
                if os.path.isdir(item_path):
                    size = get_directory_size(item_path)
                    size_mb = size / (1024**2)
                    
                    if size_mb > limit_mb:
                        large_dirs.append({
                            'path': item_path,
                            'size_mb': size_mb
                        })
            except:
                continue
    except:
        pass
    
    # 按大小排序
    large_dirs.sort(key=lambda x: x['size_mb'], reverse=True)
    return large_dirs

def get_directory_size(path):
    """获取目录大小"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_directory_size(entry.path)
    except:
        pass
    return total

def save_check_record(data):
    """保存检查记录"""
    record_file = "memory/disk_check_history.json"
    
    # 加载现有记录
    history = []
    if os.path.exists(record_file):
        try:
            with open(record_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []
    
    # 添加新记录
    history.append(data)
    
    # 只保留最近30条记录
    if len(history) > 30:
        history = history[-30:]
    
    # 保存记录
    os.makedirs(os.path.dirname(record_file), exist_ok=True)
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    print(f"\n检查记录已保存: {record_file}")

def generate_cleanup_plan(free_gb):
    """生成清理计划"""
    print("\n清理建议:")
    
    if free_gb > 50:
        print("  当前空间充足，建议定期维护即可")
        print("  建议操作:")
        print("  1. 每月清理一次临时文件")
        print("  2. 每季度整理一次下载文件夹")
        print("  3. 每年进行一次全面清理")
    
    elif free_gb > 20:
        print("  空间开始紧张，建议近期清理")
        print("  建议操作:")
        print("  1. 立即清理临时文件 (预计2-5GB)")
        print("  2. 清空回收站 (预计1-3GB)")
        print("  3. 检查下载文件夹 (预计1-10GB)")
        print("  4. 卸载不需要的程序")
    
    else:
        print("  空间严重不足，需要立即清理")
        print("  紧急操作:")
        print("  1. 运行磁盘清理工具")
        print("  2. 移动大文件到其他盘")
        print("  3. 考虑扩容或重装系统")
        print("  4. 联系技术支持")

def main():
    """主函数"""
    print("C盘容量监控系统")
    print("=" * 50)
    
    # 检查磁盘空间
    disk_info = check_disk_space()
    
    if disk_info:
        # 生成清理建议
        generate_cleanup_plan(disk_info['free_gb'])
        
        # 显示总结
        print("\n" + "=" * 50)
        print("总结:")
        print(f"  当前状态: {disk_info['status'].upper()}")
        print(f"  可用空间: {disk_info['free_gb']:.2f} GB")
        
        if disk_info['status'] == 'safe':
            print("  无需立即清理，保持定期维护即可")
        elif disk_info['status'] == 'warning':
            print("  建议近期进行清理维护")
        else:
            print("  需要立即清理，空间严重不足")
    
    print("\n监控完成")

if __name__ == "__main__":
    main()