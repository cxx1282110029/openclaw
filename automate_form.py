#!/usr/bin/env python3
"""
自动化填写表单脚本
使用 OpenClaw browser 命令自动化填写网页表单
"""

import subprocess
import time
import json
import os
import sys

def run_command(cmd, wait=True):
    """执行命令并返回结果"""
    print(f"🔧 执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ 错误: {result.stderr}")
        return None
    
    if wait:
        time.sleep(2)  # 等待命令执行完成
    
    return result.stdout

def start_edge_browser():
    """启动 Edge 浏览器"""
    print("🚀 启动 Edge 浏览器...")
    
    # 首先确保 Edge 已启动并启用 CDP
    edge_cmd = 'Start-Process "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" -ArgumentList "--remote-debugging-port=18802", "--user-data-dir=C:\\Users\\Administrator\\.openclaw\\browser\\edge\\user-data-edge"'
    run_command(edge_cmd)
    
    time.sleep(3)  # 等待浏览器启动
    
    # 检查浏览器状态
    status = run_command('openclaw browser status --browser-profile edge-cdp')
    if status and "运行中: true" in status:
        print("✅ Edge 浏览器已启动并连接")
        return True
    else:
        print("❌ Edge 浏览器启动失败")
        return False

def open_form_page():
    """打开表单测试页面"""
    print("📄 打开表单测试页面...")
    
    # 获取当前工作目录的绝对路径
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    form_file = os.path.join(workspace_dir, "form_example.html")
    
    # 使用 file:// 协议打开本地文件
    form_url = f"file:///{form_file.replace('\\', '/')}"
    
    result = run_command(f'openclaw browser open --browser-profile edge-cdp "{form_url}"')
    
    if result and "已打开:" in result:
        print(f"✅ 表单页面已打开: {form_url}")
        time.sleep(3)  # 等待页面加载
        return True
    else:
        print("❌ 打开表单页面失败")
        return False

def fill_form_field(field_id, value, field_type="text"):
    """填写表单字段"""
    print(f"📝 填写字段 {field_id}: {value}")
    
    # 首先获取页面快照找到字段的 ref
    snapshot = run_command('openclaw browser snapshot --browser-profile edge-cdp --json', wait=False)
    
    if not snapshot:
        print(f"❌ 无法获取页面快照")
        return False
    
    try:
        # 解析快照找到字段
        # 注意：实际应用中需要根据快照结构找到正确的 ref
        # 这里使用简化的方法，实际应该解析快照 JSON
        pass
    except:
        pass
    
    # 使用更直接的方法：通过 JavaScript 填写表单
    js_command = f'''
    document.getElementById('{field_id}').value = '{value}';
    document.getElementById('{field_id}').dispatchEvent(new Event('input', {{ bubbles: true }}));
    '''
    
    # 编码 JavaScript 命令
    import urllib.parse
    js_encoded = urllib.parse.quote(js_command)
    
    # 使用 evaluate 命令执行 JavaScript
    eval_cmd = f'openclaw browser evaluate --browser-profile edge-cdp --fn "{js_encoded}"'
    result = run_command(eval_cmd)
    
    if result:
        print(f"✅ 字段 {field_id} 填写成功")
        return True
    else:
        print(f"❌ 字段 {field_id} 填写失败")
        return False

def fill_form_with_data(form_data):
    """使用数据填写整个表单"""
    print("🎯 开始填写表单...")
    
    success_count = 0
    total_fields = len(form_data)
    
    for field_id, value in form_data.items():
        if fill_form_field(field_id, value):
            success_count += 1
        time.sleep(0.5)  # 字段间短暂等待
    
    print(f"📊 表单填写完成: {success_count}/{total_fields} 个字段成功")
    return success_count == total_fields

def submit_form():
    """提交表单"""
    print("📤 提交表单...")
    
    # 点击提交按钮
    js_click = '''
    document.querySelector('button[type="submit"]').click();
    '''
    
    import urllib.parse
    js_encoded = urllib.parse.quote(js_click)
    
    result = run_command(f'openclaw browser evaluate --browser-profile edge-cdp --fn "{js_encoded}"')
    
    if result:
        print("✅ 表单提交成功")
        time.sleep(2)  # 等待提交完成
        return True
    else:
        print("❌ 表单提交失败")
        return False

def take_screenshot(filename):
    """截图保存"""
    print("📸 截图保存...")
    
    # 创建截图目录
    screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    
    screenshot_path = os.path.join(screenshot_dir, filename)
    
    result = run_command(f'openclaw browser screenshot --browser-profile edge-cdp --full-page --output "{screenshot_path}"')
    
    if result and "MEDIA:" in result:
        print(f"✅ 截图已保存: {screenshot_path}")
        return True
    else:
        print("❌ 截图失败")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🤖 自动化表单填写脚本")
    print("=" * 60)
    
    # 测试数据
    test_data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "phone": "13800138000",
        "gender": "male",
        "age": "28",
        "city": "北京",
        "message": "这是一个自动化测试的留言。\n测试表单填写功能是否正常工作。",
        "agree": "true"
    }
    
    try:
        # 步骤1: 启动浏览器
        if not start_edge_browser():
            print("❌ 浏览器启动失败，退出脚本")
            return
        
        # 步骤2: 打开表单页面
        if not open_form_page():
            print("❌ 打开表单页面失败，退出脚本")
            return
        
        # 步骤3: 截图（填写前）
        take_screenshot("form_before_fill.png")
        
        # 步骤4: 填写表单
        print("\n📋 表单数据:")
        for key, value in test_data.items():
            print(f"  {key}: {value}")
        
        if not fill_form_with_data(test_data):
            print("⚠️  部分字段填写失败，继续执行...")
        
        # 步骤5: 截图（填写后）
        take_screenshot("form_after_fill.png")
        
        # 步骤6: 提交表单
        submit_form()
        
        # 步骤7: 截图（提交后）
        take_screenshot("form_after_submit.png")
        
        print("\n" + "=" * 60)
        print("🎉 自动化表单填写完成！")
        print("=" * 60)
        
        # 显示截图路径
        screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        print(f"\n📁 截图保存在: {screenshot_dir}")
        print("  1. form_before_fill.png - 填写前的表单")
        print("  2. form_after_fill.png - 填写后的表单")
        print("  3. form_after_submit.png - 提交后的表单")
        
    except Exception as e:
        print(f"\n❌ 脚本执行出错: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n🔚 脚本执行结束")

if __name__ == "__main__":
    main()