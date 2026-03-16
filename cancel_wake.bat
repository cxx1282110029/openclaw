@echo off
echo ========================================
echo  取消每天 8:15 自动唤醒
echo ========================================
echo.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 请以管理员身份运行！
    pause
    exit /b 1
)

echo 正在删除唤醒任务...
schtasks /delete /tn "WakeAt815" /f

echo.
echo 已取消自动唤醒设置
echo.
pause
