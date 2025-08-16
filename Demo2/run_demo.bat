@echo off
echo ========================================
echo    Wanderlust Working Demo (No Flask)
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo Starting the demo (No Flask required!)...
echo.
echo Open your browser and go to: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause 