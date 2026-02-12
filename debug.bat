@echo off
cd /d "%~dp0"
echo Testing Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo.
echo Testing Streamlit...
python -m streamlit --version
if errorlevel 1 (
    echo ERROR: Streamlit not installed!
    echo Try: pip install -r requirements.txt
    pause
    exit /b 1
)
echo.
echo Starting app...
python -m streamlit run app.py
echo.
echo Streamlit exited with code: %errorlevel%
pause
