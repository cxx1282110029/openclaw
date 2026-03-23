#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片水印处理工具
用于移除图片中的抖音号水印
"""

from PIL import Image, ImageDraw, ImageFilter
import os

def analyze_image(image_path):
    """分析图片基本信息"""
    try:
        img = Image.open(image_path)
        print(f"图片信息:")
        print(f"  格式: {img.format}")
        print(f"  尺寸: {img.size} (宽x高)")
        print(f"  模式: {img.mode}")
        print(f"  文件大小: {os.path.getsize(image_path)} 字节")
        
        # 检查是否有透明度通道
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            print(f"  包含透明度: 是")
        else:
            print(f"  包含透明度: 否")
            
        return img
    except Exception as e:
        print(f"打开图片失败: {e}")
        return None

def remove_watermark_simple(image_path, output_path, watermark_area=None):
    """
    简单水印移除方法
    如果知道水印位置，可以用矩形覆盖
    """
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        if watermark_area:
            # 使用提供的区域
            x1, y1, x2, y2 = watermark_area
        else:
            # 默认假设水印在右下角（常见位置）
            width, height = img.size
            x1 = width - 200  # 右下角200x50区域
            y1 = height - 50
            x2 = width
            y2 = height
        
        print(f"处理水印区域: ({x1}, {y1}) - ({x2}, {y2})")
        
        # 获取周围颜色进行填充
        if x1 > 10 and y1 > 10:
            # 取样水印区域左上角附近的颜色
            sample_color = img.getpixel((x1-5, y1-5))
        else:
            # 使用默认颜色
            sample_color = (255, 255, 255) if img.mode == 'RGB' else (255, 255, 255, 255)
        
        # 绘制矩形覆盖水印
        draw.rectangle([x1, y1, x2, y2], fill=sample_color)
        
        # 保存图片
        img.save(output_path)
        print(f"处理完成，保存到: {output_path}")
        return True
        
    except Exception as e:
        print(f"处理图片失败: {e}")
        return False

def create_preview_options(image_path):
    """创建预览选项，帮助确定水印位置"""
    try:
        img = Image.open(image_path)
        width, height = img.size
        
        print("\n常见水印位置:")
        print("1. 右下角 (常见)")
        print("2. 左下角")
        print("3. 右上角")
        print("4. 左上角")
        print("5. 底部中央")
        print("6. 顶部中央")
        
        # 常见水印区域尺寸
        common_sizes = [
            (150, 50),   # 小水印
            (200, 60),   # 中等水印
            (250, 80),   # 大水印
        ]
        
        print("\n常见水印尺寸:")
        for i, (w, h) in enumerate(common_sizes, 1):
            print(f"{i}. {w}x{h} 像素")
        
        return True
    except Exception as e:
        print(f"创建预览失败: {e}")
        return False

def main():
    """主函数"""
    input_path = "received_image.png"
    output_path = "processed_image.png"
    
    if not os.path.exists(input_path):
        print(f"图片不存在: {input_path}")
        return
    
    print("=" * 50)
    print("图片水印处理工具")
    print("=" * 50)
    
    # 分析图片
    img = analyze_image(input_path)
    if not img:
        return
    
    print("\n" + "=" * 50)
    print("处理选项")
    print("=" * 50)
    
    # 创建预览选项
    create_preview_options(input_path)
    
    print("\n由于无法自动检测水印位置，需要手动指定:")
    print("请告诉我水印的大致位置和尺寸，例如:")
    print("  - '右下角，大约200x50像素'")
    print("  - '左下角，大约150x40像素'")
    print("  - '具体坐标: (100,200)-(300,250)'")
    
    # 默认处理右下角
    print("\n将尝试处理右下角区域...")
    
    # 简单处理右下角
    success = remove_watermark_simple(input_path, output_path)
    
    if success:
        print(f"\n✅ 处理完成!")
        print(f"原始图片: {input_path}")
        print(f"处理后的图片: {output_path}")
        print(f"文件大小: {os.path.getsize(output_path)} 字节")
    else:
        print("\n❌ 处理失败")

if __name__ == "__main__":
    main()