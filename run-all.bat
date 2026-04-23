@echo off
setlocal enabledelayedexpansion
set ROOT=%~dp0
set BACKEND=%ROOT%backend
set FRONTEND=%ROOT%frontend
set PYTHON=

if exist "%BACKEND%\venv310\Scripts\python.exe" (
    set "PYTHON=%BACKEND%\venv310\Scripts\python.exe"
) else if exist "%BACKEND%\venv\Scripts\python.exe" (
    set "PYTHON=%BACKEND%\venv\Scripts\python.exe"
) else if exist "%ROOT%\.venv\Scripts\python.exe" (
    set "PYTHON=%ROOT%\.venv\Scripts\python.exe"
) else (
    where py >nul 2>&1
    if not errorlevel 1 (
        set "PYTHON=py -3.10"
    ) else (
        where python >nul 2>&1
        if not errorlevel 1 (
            set "PYTHON=python"
        )
    )
)

if "%PYTHON%"=="" (
    echo ERROR: No Python interpreter found. Install Python 3.10+.
    exit /b 1
)

start "Backend" powershell -NoExit -Command "Set-Location '%BACKEND%'; %PYTHON% -m pip install -r requirements.txt; %PYTHON% -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
start "Frontend" powershell -NoExit -Command "Set-Location '%FRONTEND%'; if not exist node_modules (npm install); npm run dev"

echo Started backend and frontend.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
endlocal