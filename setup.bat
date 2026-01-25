@echo off
REM Setup script for Voice Helper Application (Windows)

echo Voice Helper - Setup Script
echo ============================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Python not found! Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist "venv\" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing Python dependencies...
echo This may take several minutes...
pip install -r requirements.txt

echo.
echo ============================
echo Setup complete!
echo.
echo To run the application:
echo   1. Activate the virtual environment: venv\Scripts\activate.bat
echo   2. Run the app: python main.py
echo.
echo Note: You may need to install FFmpeg separately from https://ffmpeg.org/
echo.
pause
