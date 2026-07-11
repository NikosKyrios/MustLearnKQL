@echo off
REM Must Learn KQL Learning Hub - Windows Startup Script

echo.
echo 🔍 Must Learn KQL Learning Hub
echo ====================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✓ Python found
python --version

REM Check if virtual environment exists
if not exist "venv\" (
    echo.
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
)

REM Check for .env file
if not exist ".env" (
    echo.
    echo ⚠️  No .env file found. Creating from template...
    copy .env.example .env
    echo.
    echo ⚙️  Please edit .env and add your Grok API key:
    echo    XAI_API_KEY=your_key_here
    echo.
    pause
)

echo.
echo 🚀 Starting Must Learn KQL Learning Hub...
echo    The app will open in your browser at http://localhost:8501
echo.
echo    Press Ctrl+C to stop the server
echo.

REM Run the app
streamlit run app.py

pause
