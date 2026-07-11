@echo off
title Smart Expense Tracker - Web Server
echo =========================================================
echo   Smart Expense Tracker - Startup Web Service
echo =========================================================
echo.

:: Check if virtual environment exists in current folder
if exist .venv\Scripts\activate.bat (
    echo [INFO] Activating virtual environment (.venv)...
    call .venv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    echo [INFO] Activating virtual environment (venv)...
    call venv\Scripts\activate.bat
) else (
    echo [INFO] No local virtual environment detected.
    echo [INFO] Running with system-wide python installer.
)

:: Verify Flask dependency and install if missing
echo [INFO] Verifying Flask installation status...
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Flask not found. Installing Flask framework via pip...
    pip install flask
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Flask. Please run: pip install flask manually.
        pause
        exit /b %errorlevel%
    )
) else (
    echo [INFO] Flask dependency verified successfully.
)

echo.
echo ---------------------------------------------------------
echo   SUCCESS: Web Application server is launching!
echo   Open your browser and navigate to:
echo.
echo   >>> http://127.0.0.1:5000 <<<
echo ---------------------------------------------------------
echo.

python app.py
pause
