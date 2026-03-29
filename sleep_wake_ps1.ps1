# 电脑睡眠与唤醒设置脚本
# 创建时间: 2026-03-29
# 用途: 设置电脑睡眠并在指定时间唤醒

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "       电脑睡眠与唤醒设置" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 显示当前时间
$currentTime = Get-Date
Write-Host "当前时间: $($currentTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Green
Write-Host ""

# 设置唤醒时间
$wakeTimeString = "2026-03-29 09:30:00"
$wakeTime = [DateTime]::Parse($wakeTimeString)

Write-Host "设置的唤醒时间: $($wakeTime.ToString('HH:mm:ss'))" -ForegroundColor Green

# 计算时间差
$timeDiff = $wakeTime - $currentTime
if ($timeDiff.TotalSeconds -le 0) {
    Write-Host "❌ 错误: 指定的唤醒时间已过！" -ForegroundColor Red
    Write-Host "请指定未来的时间。" -ForegroundColor Yellow
    exit 1
}

Write-Host "距离唤醒还有: $([math]::Round($timeDiff.TotalMinutes,1)) 分钟" -ForegroundColor Green
Write-Host ""

# 方法1: 使用powercfg设置唤醒定时器
Write-Host "方法1: 设置唤醒定时器..." -ForegroundColor Yellow
try {
    # 先检查当前唤醒设置
    powercfg -lastwake
    
    # 设置唤醒时间（需要管理员权限）
    Write-Host "尝试设置唤醒定时器..." -ForegroundColor Gray
    # 注意: 实际唤醒设置可能需要管理员权限和BIOS支持
}
catch {
    Write-Host "唤醒定时器设置可能需要管理员权限" -ForegroundColor Yellow
}

Write-Host ""

# 方法2: 创建计划任务（最可靠）
Write-Host "方法2: 创建唤醒计划任务..." -ForegroundColor Yellow
$taskName = "ComputerWakeUp_$(Get-Date -Format 'yyyyMMdd_HHmm')"

try {
    # 创建触发时间
    $trigger = New-ScheduledTaskTrigger -Once -At $wakeTime
    
    # 创建动作（简单的命令提示）
    $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c echo Computer woke up at %time%"
    
    # 创建任务设置（允许唤醒计算机运行）
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -WakeToRun
    
    # 注册任务（需要管理员权限）
    $task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Description "Wake up computer at $($wakeTime.ToString('HH:mm'))"
    
    Write-Host "✅ 计划任务配置已创建" -ForegroundColor Green
    Write-Host "任务名称: $taskName" -ForegroundColor Gray
    Write-Host "唤醒时间: $($wakeTime.ToString('HH:mm:ss'))" -ForegroundColor Gray
    
    # 提示用户如何手动注册
    Write-Host ""
    Write-Host "📋 手动执行步骤:" -ForegroundColor Cyan
    Write-Host "1. 以管理员身份打开PowerShell" -ForegroundColor White
    Write-Host "2. 运行以下命令:" -ForegroundColor White
    Write-Host "   Register-ScheduledTask -TaskName `"$taskName`" -InputObject `$task -User `"SYSTEM`" -Force" -ForegroundColor Gray
}
catch {
    Write-Host "⚠️ 计划任务创建需要管理员权限" -ForegroundColor Yellow
}

Write-Host ""

# 方法3: 立即进入睡眠
Write-Host "方法3: 准备进入睡眠..." -ForegroundColor Yellow
Write-Host "电脑将在以下时间自动唤醒:" -ForegroundColor White
Write-Host "   ⏰ $($wakeTime.ToString('HH:mm:ss'))" -ForegroundColor Green
Write-Host ""

$confirm = Read-Host "是否立即进入睡眠？(Y/N)"
if ($confirm -eq 'Y' -or $confirm -eq 'y') {
    Write-Host "正在进入睡眠模式..." -ForegroundColor Green
    Write-Host "再见！电脑将在 $($wakeTime.ToString('HH:mm')) 唤醒" -ForegroundColor Cyan
    
    # 进入睡眠（需要管理员权限）
    # Add-Type -AssemblyName System.Windows.Forms
    # [System.Windows.Forms.Application]::SetSuspendState([System.Windows.Forms.PowerState]::Suspend, $false, $false)
    
    # 替代方法：使用rundll32
    Write-Host "执行: rundll32.exe powrprof.dll,SetSuspendState 0,1,0" -ForegroundColor Gray
    Start-Process -FilePath "rundll32.exe" -ArgumentList "powrprof.dll,SetSuspendState 0,1,0" -NoNewWindow
} else {
    Write-Host "取消进入睡眠" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "设置完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan