# OpenClaw Windows Service 配置脚本
# 创建者：一拳先生
# 日期：2026-03-23

# 1. 停止现有服务（如果存在）
Write-Host "检查现有OpenClaw服务..." -ForegroundColor Cyan
$service = Get-Service -Name "OpenClaw" -ErrorAction SilentlyContinue
if ($service) {
    Write-Host "找到现有服务，正在停止..." -ForegroundColor Yellow
    Stop-Service -Name "OpenClaw" -Force
    sc.exe delete "OpenClaw"
    Start-Sleep -Seconds 2
}

# 2. 创建服务
Write-Host "创建OpenClaw Windows服务..." -ForegroundColor Cyan
$nodePath = "D:\nodejs\node.exe"
$scriptPath = "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw-cn\dist\entry.js"
$serviceName = "OpenClaw"
$displayName = "OpenClaw AI Assistant"
$description = "OpenClaw AI助手服务，提供智能对话、任务管理、系统监控等功能"

# 创建服务
New-Service -Name $serviceName `
    -DisplayName $displayName `
    -Description $description `
    -BinaryPathName "`"$nodePath`" `"$scriptPath`" gateway --port 18789" `
    -StartupType Automatic `
    -ErrorAction Stop

Write-Host "服务创建成功！" -ForegroundColor Green

# 3. 配置服务恢复选项
Write-Host "配置服务恢复选项..." -ForegroundColor Cyan
sc.exe failure $serviceName reset= 86400 actions= restart/5000/restart/10000/restart/30000
sc.exe failureflag $serviceName 1

# 4. 启动服务
Write-Host "启动OpenClaw服务..." -ForegroundColor Cyan
Start-Service -Name $serviceName
Start-Sleep -Seconds 3

# 5. 验证服务状态
Write-Host "验证服务状态..." -ForegroundColor Cyan
$serviceStatus = Get-Service -Name $serviceName
Write-Host "服务名称: $($serviceStatus.Name)" -ForegroundColor Yellow
Write-Host "显示名称: $($serviceStatus.DisplayName)" -ForegroundColor Yellow
Write-Host "状态: $($serviceStatus.Status)" -ForegroundColor Green
Write-Host "启动类型: $($serviceStatus.StartType)" -ForegroundColor Yellow

# 6. 测试服务连接
Write-Host "测试服务连接..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:18789/" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ 服务连接正常！" -ForegroundColor Green
    Write-Host "Dashboard地址: http://127.0.0.1:18789/" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️ 服务连接测试失败，但服务已启动" -ForegroundColor Yellow
    Write-Host "错误信息: $_" -ForegroundColor Red
}

# 7. 创建快捷方式
Write-Host "创建管理快捷方式..." -ForegroundColor Cyan
$shortcutPath = "$env:USERPROFILE\Desktop\OpenClaw管理.lnk"
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-NoExit -Command `"& {Get-Service -Name 'OpenClaw' | Format-List; Write-Host '`n管理命令:'; Write-Host '启动服务: Start-Service -Name OpenClaw'; Write-Host '停止服务: Stop-Service -Name OpenClaw'; Write-Host '重启服务: Restart-Service -Name OpenClaw'; Write-Host '查看日志: Get-EventLog -LogName Application -Source OpenClaw -Newest 10';}`""
$Shortcut.WorkingDirectory = "$env:USERPROFILE"
$Shortcut.WindowStyle = 1
$Shortcut.Description = "OpenClaw服务管理"
$Shortcut.Save()

Write-Host "`n✅ OpenClaw Windows服务配置完成！" -ForegroundColor Green
Write-Host "`n📋 服务信息：" -ForegroundColor Cyan
Write-Host "   服务名称: OpenClaw" -ForegroundColor Yellow
Write-Host "   端口: 18789" -ForegroundColor Yellow
Write-Host "   Dashboard: http://127.0.0.1:18789/" -ForegroundColor Yellow
Write-Host "   管理快捷方式: 桌面上的'OpenClaw管理.lnk'" -ForegroundColor Yellow
Write-Host "`n🔧 管理命令：" -ForegroundColor Cyan
Write-Host "   启动: Start-Service -Name OpenClaw" -ForegroundColor White
Write-Host "   停止: Stop-Service -Name OpenClaw" -ForegroundColor White
Write-Host "   重启: Restart-Service -Name OpenClaw" -ForegroundColor White
Write-Host "   状态: Get-Service -Name OpenClaw" -ForegroundColor White
Write-Host "`n📝 日志查看：" -ForegroundColor Cyan
Write-Host "   Get-EventLog -LogName Application -Source OpenClaw -Newest 10" -ForegroundColor White