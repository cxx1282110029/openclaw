@echo off
chcp 65001 >nul
echo 🤖 自动化表单填写脚本
echo ========================

REM 1. 检查 Edge 浏览器状态
echo 🚀 检查 Edge 浏览器状态...
openclaw browser status --browser-profile edge-cdp | findstr "运行中: true"
if errorlevel 1 (
    echo 启动 Edge 浏览器...
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=18802 --user-data-dir="C:\Users\Administrator\.openclaw\browser\edge\user-data-edge"
    timeout /t 5 /nobreak >nul
)

REM 2. 打开表单测试页面
echo 📄 打开表单测试页面...
set "FORM_FILE=C:\Users\Administrator\.openclaw\workspace\form_example.html"
set "FORM_URL=file:///%FORM_FILE:\=/%"
openclaw browser open --browser-profile edge-cdp "%FORM_URL%"
timeout /t 3 /nobreak >nul

REM 3. 截图（填写前）
echo 📸 截图（填写前）...
openclaw browser screenshot --browser-profile edge-cdp --full-page --output "form_before_fill.png"
timeout /t 2 /nobreak >nul

REM 4. 填写表单字段
echo 📝 开始填写表单...

echo   填写姓名: 张三
openclaw browser evaluate --browser-profile edge-cdp --fn "document.getElementById('name').value = '张三'; document.getElementById('name').dispatchEvent(new Event('input', { bubbles: true }));"
timeout /t 1 /nobreak >nul

echo   填写邮箱: zhangsan@example.com
openclaw browser evaluate --browser-profile edge-cdp --fn "document.getElementById('email').value = 'zhangsan@example.com'; document.getElementById('email').dispatchEvent(new Event('input', { bubbles: true }));"
timeout /t 1 /nobreak >nul

echo   填写电话: 13800138000
openclaw browser evaluate --browser-profile edge-cdp --fn "document.getElementById('phone').value = '13800138000'; document.getElementById('phone').dispatchEvent(new Event('input', { bubbles: true }));"
timeout /t 1 /nobreak >nul

echo   选择性别: 男
openclaw browser evaluate --browser-profile edge-cdp --fn "document.getElementById('gender').value = 'male'; document.getElementById('gender').dispatchEvent(new Event('change', { bubbles: true }));"
timeout /t 1 /nobreak >nul

echo   填写年龄: 28
openclaw browser evaluate --browser-profile edge-cdp --fn "document.getElementById('age').value = '28'; document.getElementById('age').dispatchEvent(new Event('input', { bubbles: true }));"
timeout /t 1 /nobreak >nul

echo   填写城市: 北京
openclaw browser evaluate --browser-profile edge-cdp --fn "document.getElementById('city').value = '北京'; document.getElementById('city').dispatchEvent(new Event('input', { bubbles: true }));"
timeout /t 1 /nobreak >nul

echo   填写留言: 自动化测试留言
openclaw browser evaluate --browser-profile edge-cdp --fn "document.getElementById('message').value = '这是一个自动化测试的留言。\n测试表单填写功能是否正常工作。'; document.getElementById('message').dispatchEvent(new Event('input', { bubbles: true }));"
timeout /t 1 /nobreak >nul

echo   勾选同意条款
openclaw browser evaluate --browser-profile edge-cdp --fn "document.getElementById('agree').checked = true; document.getElementById('agree').dispatchEvent(new Event('change', { bubbles: true }));"
timeout /t 1 /nobreak >nul

REM 5. 截图（填写后）
echo 📸 截图（填写后）...
openclaw browser screenshot --browser-profile edge-cdp --full-page --output "form_after_fill.png"
timeout /t 2 /nobreak >nul

REM 6. 提交表单
echo 📤 提交表单...
openclaw browser evaluate --browser-profile edge-cdp --fn "document.querySelector('button[type=\"submit\"]').click();"
timeout /t 3 /nobreak >nul

REM 7. 截图（提交后）
echo 📸 截图（提交后）...
openclaw browser screenshot --browser-profile edge-cdp --full-page --output "form_after_submit.png"
timeout /t 2 /nobreak >nul

echo.
echo 🎉 自动化表单填写完成！
echo ========================
echo.
echo 📁 生成的截图文件：
echo   1. form_before_fill.png - 填写前的表单
echo   2. form_after_fill.png - 填写后的表单
echo   3. form_after_submit.png - 提交后的表单
echo.
echo 🔍 查看页面快照：
echo   openclaw browser snapshot --browser-profile edge-cdp
echo.
echo 🔄 重新运行脚本：
echo   automate_form.bat
pause