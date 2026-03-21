# Windows TTS 测试脚本
Write-Host "开始测试Windows语音合成功能..."

try {
    # 加载语音合成程序集
    Add-Type -AssemblyName System.Speech
    
    # 创建语音合成器
    $speech = New-Object System.Speech.Synthesis.SpeechSynthesizer
    
    # 测试中文语音
    Write-Host "正在合成中文语音..."
    $speech.Speak("龙虾机器人已启动，贾维斯模式激活")
    
    # 测试英文语音
    Write-Host "正在合成英文语音..."
    $speech.Speak("OpenClaw is ready, voice wakeup enabled")
    
    Write-Host "语音合成测试完成！"
} catch {
    Write-Host "错误: $_"
    Write-Host "可能的原因："
    Write-Host "1. System.Speech程序集未安装"
    Write-Host "2. 语音合成功能被禁用"
    Write-Host "3. 权限问题"
}