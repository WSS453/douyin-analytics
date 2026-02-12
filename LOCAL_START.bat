@echo off
cd /d "%~dp0"
echo ========================================
echo    抖音博主数据分析系统 - 本地版本
echo ========================================
echo.
echo 1. 安装依赖: pip install -r requirements.txt
echo 2. 安装浏览器: python -m playwright install chromium
echo 3. 运行应用: python local_app.py
echo.
echo 直接启动应用...
echo.
echo 请访问: http://localhost:8501
echo.
echo 按 Ctrl+C 停止应用
echo ========================================
echo.
python local_app.py
pause
