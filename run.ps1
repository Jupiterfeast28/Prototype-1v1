# PowerShell script to run PathAI website
Write-Host "Starting PathAI Website..." -ForegroundColor Green
Write-Host ""

Set-Location backend

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check/Create virtual environment
Write-Host "Checking virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path .venv)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing/updating dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python init_db.py

Write-Host ""
Write-Host "Starting Flask server..." -ForegroundColor Green
Write-Host "Open http://localhost:5000 in your browser" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python app.py

