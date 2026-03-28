#!/bin/bash
# 基本浏览器导航示例

echo "启动浏览器..."
openclaw browser start

echo "打开百度..."
openclaw browser open https://baidu.com

sleep 3

echo "截图..."
openclaw browser screenshot --full-page --output baidu-screenshot.png

echo "获取页面快照..."
openclaw browser snapshot --format ai --limit 100

echo "操作完成"