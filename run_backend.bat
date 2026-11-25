@echo off
cd /d "%~dp0backend"
set PYTHONPATH=%cd%
"C:\Users\Nitin kumar\AppData\Local\Programs\Python\Python313\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
