@echo off
echo Installing dependencies...
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Installation failed!
    pause
    exit /b
)
echo.
echo Dependencies installed successfully!
pause
