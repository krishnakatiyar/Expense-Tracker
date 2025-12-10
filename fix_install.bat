@echo off
echo Fixing Python Pip installation...
py -m ensurepip --default-pip
if %errorlevel% neq 0 (
    echo.
    echo ensurepip failed. Trying to upgrade...
    py -m ensurepip --upgrade
)

echo.
echo Installing dependencies...
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Installation failed!
    pause
    exit /b
)

echo.
echo All fixed! You can now run the app.
pause
