@echo off
if not exist mlenv (
    python -m venv mlenv
)
call mlenv\Scripts\activate
if exist requirements.txt (
    pip install -r requirements.txt -i https://mirror2.chabokan.net/pypi/simple/ --trusted-host mirror2.chabokan.net
)
echo Starting server and browser...
start /b cmd /c "timeout /t 3 >nul && start http://127.0.0.1:8000/login"
uvicorn src.main:app --reload