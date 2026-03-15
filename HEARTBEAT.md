# HEARTBEAT.md - 项目巡检
# 运行频率: 每30分钟
# 最后更新: 2026-03-15

## 执行检查任务
运行 `python heartbeat_tasks.py` 执行所有检查

## 检查项目

### 1. 智能人工生命体 "L" 项目
- 路径: `E:\L-Intelligence`
- 检查: 是否有错误日志、核心文件是否存在

### 2. 股票实时监控系统  
- 路径: `E:\StockMonitor`
- 检查: 数据库是否更新、程序是否运行

### 3. Memory 文件检查
- 自动创建今天的 memory/YYYY-MM-DD.md

### 4. Gateway 状态检查
- 运行 `openclaw gateway status`
- 异常时告警

### 5. Git 备份检查
- 检查未提交文件，提醒备份

## 告警机制
- 状态变化时才会通知
- 相同告警有冷却时间（1-4小时）
- 状态记录在 `memory/heartbeat-state.json`
