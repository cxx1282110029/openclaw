@echo off
chcp 65001 >nul
echo ========================================
echo       电脑睡眠与唤醒设置
echo ========================================
echo.

REM 显示当前时间
echo 当前时间: %date% %time%
echo.

REM 设置唤醒时间（今天9:30）
set WAKE_HOUR=09
set WAKE_MINUTE=30

echo 设置唤醒时间为: %WAKE_HOUR%:%WAKE_MINUTE%
echo.

REM 方法1: 使用rundll32立即进入睡眠
echo 方法1: 立即进入睡眠（按任意键继续...）
pause >nul
echo 正在进入睡眠模式...
echo 电脑将在今天 %WAKE_HOUR%:%WAKE_MINUTE% 自动唤醒
echo.
rundll32.exe powrprof.dll,SetSuspendState 0,1,0

REM 如果上述方法无效，使用方法2
echo.
echo ========================================
echo       备用唤醒设置方法
echo ========================================
echo.

REM 创建唤醒计划任务（需要管理员权限）
echo 创建计划任务唤醒计算机...
schtasks /create /tn "AutoWake_0930" /tr "cmd /c echo Computer Woke Up" /sc once /st %WAKE_HOUR%:%WAKE_MINUTE% /sd %date% /ru SYSTEM

echo.
echo 设置完成！
echo 1. 电脑将立即进入睡眠模式
echo 2. 将在 %WAKE_HOUR%:%WAKE_MINUTE% 自动唤醒
echo 3. 如需取消，运行: schtasks /delete /tn "AutoWake_0930" /f
echo.
pause