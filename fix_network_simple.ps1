# 简单网络修复脚本
Write-Host "网络修复开始..." -ForegroundColor Cyan

# 1. 刷新DNS
Write-Host "刷新DNS缓存..." -ForegroundColor Yellow
ipconfig /flushdns
Write-Host "DNS缓存已刷新" -ForegroundColor Green

# 2. 重置Winsock
Write-Host "重置网络堆栈..." -ForegroundColor Yellow
netsh winsock reset 2>$null
netsh int ip reset 2>$null
Write-Host "网络堆栈已重置" -ForegroundColor Green

# 3. 测试连接
Write-Host "测试连接..." -ForegroundColor Yellow

# 测试TCP连接
$test1 = Test-NetConnection -ComputerName "baidu.com" -Port 443 -InformationLevel Quiet -ErrorAction SilentlyContinue
if ($test1) {
    Write-Host "百度HTTPS: ✅ 连接成功" -ForegroundColor Green
} else {
    Write-Host "百度HTTPS: ❌ 连接失败" -ForegroundColor Red
}

# 测试天气API
try {
    $response = Invoke-RestMethod -Uri "https://60s.viki.moe/v2/weather?query=北京" -TimeoutSec 5 -ErrorAction SilentlyContinue
    Write-Host "天气API: ✅ 连接成功" -ForegroundColor Green
} catch {
    Write-Host "天气API: ❌ 连接失败" -ForegroundColor Red
}

# 4. 显示当前IP
Write-Host "`n当前网络信息:" -ForegroundColor Cyan
ipconfig | findstr "IPv4" | Select-Object -First 3

Write-Host "`n修复完成！" -ForegroundColor Cyan
Write-Host "如果仍有问题，请尝试重启计算机。" -ForegroundColor Yellow