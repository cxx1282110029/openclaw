@echo off
echo ========================================
echo  Setup Daily Wake at 8:15
echo ========================================
echo.

:: Check admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Please run as administrator!
    echo Right-click - Run as administrator
    pause
    exit /b 1
)

echo [1/3] Creating wake task...
schtasks /create /tn "WakeAt815" /tr "cmd /c echo Wake up at 8:15" /sc daily /st 08:15 /ru SYSTEM /f
if %errorlevel% equ 0 (
    echo  Task created successfully!
) else (
    echo  Task may already exist or failed to create
)

echo.
echo [2/3] Enabling wake timers...
powercfg /SETACVALUEINDEX SCHEME_CURRENT SUB_SLEEP RTCWAKE 1
powercfg /SETDCVALUEINDEX SCHEME_CURRENT SUB_SLEEP RTCWAKE 1
powercfg /SETACTIVE SCHEME_CURRENT
echo  Wake timers enabled

echo.
echo [3/3] Checking current wake settings...
powercfg /WAKETIMERS

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Computer will wake up at 8:15 daily
echo.
echo Note:
echo - PC must be in Sleep or Hibernate mode
echo - Will not work if fully shutdown
echo - To cancel, run: schtasks /delete /tn "WakeAt815" /f
echo.
pause
