@echo off
echo ========================================
echo    Wanderlust Price Prediction Demo
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo.
python install_deps.py

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo Testing the demo...
echo.
python test_demo.py

if errorlevel 1 (
    echo.
    echo Some tests failed. Please check the errors above.
) else (
    echo.
    echo All tests passed! The demo is ready to use.
    echo.
    echo To use the demo:
    echo 1. Open index.html in your browser
    echo 2. Fill the form and download data
    echo 3. Run: python run_prediction.py "image.jpg" "location" "country"
)

pause 