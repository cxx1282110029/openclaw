@echo off
echo ========================================
echo  Setup Auto Sleep at 23:00 + Wake at 8:15
echo ========================================
echo.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Please run as administrator!
    pause
    exit /b 1
)

echo [1/2] Creating sleep task at 23:00...
schtasks /create /tn "SleepAt2300" /tr "rundll32.exe powrprof.dll,SetSuspendState 0,0,0" /sc daily /st 23:00 /ru SYSTEM /f
echo  Sleep task created

echo.
echo [2/2] Checking wake task...
schtasks /query /tn "WakeAt815" >nul 2>&1
if %errorlevel% neq 0 (
    echo  Creating wake task at 8:15...
    schtasks /create /tn "WakeAt815" /tr "cmd /c echo Wake" /sc daily /st 08:15 /ru SYSTEM /f
) else (
    echo  Wake task already exists
)

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Daily schedule:
echo   23:00 - Auto Sleep (not hibernate)
echo   08:15 - Auto Wake up
echo.
echo To cancel:
echo   schtasks /delete /tn "SleepAt2300" /f
pause
