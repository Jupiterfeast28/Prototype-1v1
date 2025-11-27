@echo off
echo Starting PathAI Website...
echo.

cd backend

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Checking virtual environment...
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing/updating dependencies...
pip install -q -r requirements.txt

echo Initializing database...
python init_db.py

echo.
echo Starting Flask server...
echo Open http://localhost:5000 in your browser
echo Press Ctrl+C to stop the server
echo.

python app.py

pause

