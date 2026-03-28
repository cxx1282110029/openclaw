# 网络连接修复脚本
# 创建时间: 2026-03-28
# 用途: 修复外部网络连接问题

Write-Host "=== 网络连接修复脚本开始 ===" -ForegroundColor Cyan

# 1. 停止可能冲突的服务
Write-Host "1. 停止冲突服务..." -ForegroundColor Yellow
$services = @("Tailscale", "WpnService", "WpnUserService_4d497")
foreach ($service in $services) {
    try {
        Stop-Service -Name $service -Force -ErrorAction SilentlyContinue
        Write-Host "   $service : 已停止" -ForegroundColor Green
    } catch {
        Write-Host "   $service : 未运行或不存在" -ForegroundColor Gray
    }
}

# 2. 设置网络接口优先级
Write-Host "`n2. 优化网络接口优先级..." -ForegroundColor Yellow
$interfaces = @(
    @{Name="WLAN"; Metric=1},
    @{Name="以太网"; Metric=10},
    @{Name="Tailscale"; Metric=100},
    @{Name="vEthernet (WSL)"; Metric=1000}
)

foreach ($iface in $interfaces) {
    try {
        Get-NetIPInterface -InterfaceAlias $iface.Name -ErrorAction SilentlyContinue | 
            Set-NetIPInterface -InterfaceMetric $iface.Metric -ErrorAction SilentlyContinue
        Write-Host "   $($iface.Name) : 优先级设置为 $($iface.Metric)" -ForegroundColor Green
    } catch {
        Write-Host "   $($iface.Name) : 接口不存在" -ForegroundColor Gray
    }
}

# 3. 刷新DNS缓存
Write-Host "`n3. 刷新DNS缓存..." -ForegroundColor Yellow
ipconfig /flushdns
Write-Host "   DNS缓存已刷新" -ForegroundColor Green

# 4. 重置Winsock
Write-Host "`n4. 重置网络堆栈..." -ForegroundColor Yellow
netsh winsock reset
netsh int ip reset
Write-Host "   网络堆栈已重置" -ForegroundColor Green

# 5. 测试连接
Write-Host "`n5. 测试网络连接..." -ForegroundColor Yellow
$testTargets = @(
    @{Name="百度"; Host="baidu.com"},
    @{Name="天气API"; Host="60s.viki.moe"},
    @{Name="GitHub"; Host="github.com"},
    @{Name="Google DNS"; Host="8.8.8.8"}
)

foreach ($test in $testTargets) {
    try {
        $tcpTest = Test-NetConnection -ComputerName $test.Host -Port 443 -InformationLevel Quiet -ErrorAction SilentlyContinue
        if ($tcpTest) {
            Write-Host "   $($test.Name) : ✅ TCP连接成功" -ForegroundColor Green
        } else {
            Write-Host "   $($test.Name) : ❌ TCP连接失败" -ForegroundColor Red
        }
    } catch {
        Write-Host "   $($test.Name) : ❌ 测试失败" -ForegroundColor Red
    }
}

# 6. 创建hosts文件备份（如果需要）
Write-Host "`n6. 检查hosts文件..." -ForegroundColor Yellow
$hostsPath = "C:\Windows\System32\drivers\etc\hosts"
if (Test-Path $hostsPath) {
    $backupPath = "$env:TEMP\hosts.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $hostsPath $backupPath -ErrorAction SilentlyContinue
    Write-Host "   hosts文件已备份到: $backupPath" -ForegroundColor Green
} else {
    Write-Host "   hosts文件不存在" -ForegroundColor Yellow
}

Write-Host "`n=== 修复完成 ===" -ForegroundColor Cyan
Write-Host "建议重启计算机以使所有更改生效" -ForegroundColor Yellow
Write-Host "脚本位置: $PSCommandPath" -ForegroundColor Gray