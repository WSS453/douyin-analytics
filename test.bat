@echo off
cd /d "%~dp0"
echo Testing Python...
python --version
if errorlevel 1 (
    echo Python not found, trying python3...
    python3 --version
)
echo.
echo Starting Streamlit...
python -m streamlit run app.py
pause
