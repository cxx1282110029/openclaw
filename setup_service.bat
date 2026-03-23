@echo off
chcp 65001 >nul
echo ========================================
echo    OpenClaw Windows 服务配置工具
echo ========================================
echo.

echo [1/6] 检查现有服务...
sc query "OpenClaw" >nul 2>&1
if %errorlevel% equ 0 (
    echo 找到现有OpenClaw服务，正在停止...
    net stop OpenClaw >nul 2>&1
    sc delete OpenClaw >nul 2>&1
    timeout /t 2 /nobreak >nul
)

echo [2/6] 创建OpenClaw服务...
set NODE_PATH=D:\nodejs\node.exe
set SCRIPT_PATH=C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw-cn\dist\entry.js
set SERVICE_NAME=OpenClaw
set DISPLAY_NAME=OpenClaw AI Assistant
set DESCRIPTION=OpenClaw AI助手服务，提供智能对话、任务管理、系统监控等功能

sc create %SERVICE_NAME% binPath= "\"%NODE_PATH%\" \"%SCRIPT_PATH%\" gateway --port 18789" DisplayName= "%DISPLAY_NAME%" start= auto

if %errorlevel% neq 0 (
    echo ❌ 服务创建失败！
    pause
    exit /b 1
)

echo [3/6] 配置服务描述...
sc description %SERVICE_NAME% "%DESCRIPTION%"

echo [4/6] 配置服务恢复选项...
sc failure %SERVICE_NAME% reset= 86400 actions= restart/5000/restart/10000/restart/30000

echo [5/6] 启动服务...
net start %SERVICE_NAME%

if %errorlevel% neq 0 (
    echo ⚠️ 服务启动失败，但已创建。请手动检查。
) else (
    echo ✅ 服务启动成功！
)

echo [6/6] 验证服务状态...
sc query %SERVICE_NAME%

echo.
echo ========================================
echo           配置完成！
echo ========================================
echo.
echo 📋 服务信息：
echo    服务名称: %SERVICE_NAME%
echo    显示名称: %DISPLAY_NAME%
echo    端口: 18789
echo    Dashboard: http://127.0.0.1:18789/
echo.
echo 🔧 管理命令：
echo    启动服务: net start OpenClaw
echo    停止服务: net stop OpenClaw
echo    重启服务: net stop OpenClaw && net start OpenClaw
echo    删除服务: sc delete OpenClaw
echo.
echo 📝 开机自启动已启用
echo 🔄 崩溃自动重启已配置（最多3次）
echo.
pause