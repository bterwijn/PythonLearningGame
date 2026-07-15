@echo off
REM Setup script for PythonLearningGame (Windows)

if exist venv (
  echo Virtual environment already exists.
) else (
  echo Creating virtual environment...
  python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo Virtual environment is active. To run the game:
echo   python main.py
echo.
echo To deactivate the virtual environment later:
echo   deactivate
pause
