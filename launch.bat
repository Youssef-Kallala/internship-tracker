@echo off
cd /d "%~dp0"
call venv\Scripts\activate
start /b python app.py
timeout /t 2 >nul
start http://127.0.0.1:5000