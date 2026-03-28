---
name: Agent Browser
description: 浏览器自动化技能，用于控制 Chrome/Chromium 浏览器，支持页面导航、截图、表单填写等自动化操作。
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["openclaw"]},"install":[{"id":"openclaw","kind":"node","package":"openclaw-cn","bins":["openclaw"],"label":"Install OpenClaw CLI (npm)"}]}}
---

# Agent Browser Skill

## 描述
浏览器自动化技能，用于控制 Chrome/Chromium 浏览器，支持页面导航、截图、表单填写等自动化操作。

## 使用方法
当用户需要浏览器自动化时使用此技能，包括：
- 打开网页并获取内容
- 填写表单并提交
- 截图保存
- 页面交互自动化

## 工具依赖
- `browser` 工具（OpenClaw 内置）

## 示例命令
```bash
# 打开浏览器
openclaw browser start

# 打开网页
openclaw browser open https://example.com

# 截图
openclaw browser screenshot --full-page

# 获取页面快照
openclaw browser snapshot
```

## 常用操作

### 1. 基本导航
```bash
# 启动浏览器
openclaw browser start

# 打开新标签页
openclaw browser open https://google.com

# 导航当前标签页
openclaw browser navigate https://github.com
```

### 2. 页面操作
```bash
# 获取页面快照（AI可读格式）
openclaw browser snapshot

# 获取无障碍树
openclaw browser snapshot --format aria

# 截图
openclaw browser screenshot
openclaw browser screenshot --full-page

# 保存为PDF
openclaw browser pdf
```

### 3. 交互操作
```bash
# 点击元素（使用快照中的ref）
openclaw browser click 12

# 输入文本
openclaw browser type 23 "搜索内容"

# 按键操作
openclaw browser press Enter

# 选择下拉选项
openclaw browser select 9 "选项1"
```

### 4. 表单填写
```bash
# 填写表单字段
openclaw browser fill --fields '[{"ref":"1","value":"用户名"},{"ref":"2","value":"密码"}]'

# 上传文件
openclaw browser upload /path/to/file.pdf
```

### 5. 等待与条件
```bash
# 等待文本出现
openclaw browser wait --text "加载完成"

# 等待选择器
openclaw browser wait --selector ".loaded"

# 等待时间
openclaw browser wait --time 5000
```

## 配置
确保在 `~/.openclaw/openclaw.json` 中配置了浏览器控制：
```json
{
  "browser": {
    "enabled": true,
    "profile": "default"
  }
}
```

## 故障排除

### 浏览器无法启动
1. 检查 Chrome/Chromium 是否已安装
2. 确保有可用的浏览器配置文件
3. 尝试重置配置文件：`openclaw browser reset-profile`

### 快照为空
1. 确保页面已加载完成
2. 使用 `--wait` 参数等待加载
3. 检查网络连接

### 元素无法点击
1. 确认 ref 是否正确
2. 元素可能被遮挡或隐藏
3. 尝试先滚动到视图：`openclaw browser scrollintoview <ref>`

## 高级功能

### 录制操作
```bash
# 开始录制追踪
openclaw browser trace start

# 执行操作...

# 停止录制并保存
openclaw browser trace stop --save /path/to/trace.zip
```

### 网络监控
```bash
# 获取控制台消息
openclaw browser console

# 获取网络请求
openclaw browser requests

# 获取页面错误
openclaw browser errors
```

### 存储操作
```bash
# 读取cookies
openclaw browser cookies get

# 设置localStorage
openclaw browser storage set --key "token" --value "abc123"
```

## 注意事项
1. 浏览器自动化需要 Chrome/Chromium 浏览器
2. 某些网站可能有反自动化措施
3. 复杂操作建议分步进行并添加等待
4. 定期清理浏览器缓存和配置文件