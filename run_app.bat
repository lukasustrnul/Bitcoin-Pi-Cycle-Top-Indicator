@echo off
REM ------------------------------------------------------------
REM Local launcher for Bitcoin Pi Cycle Top Indicator (Streamlit)
REM Assumes a virtual environment exists in .venv next to this file.
REM ------------------------------------------------------------

REM Activate virtual environment (required for project dependencies).
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Unable to activate .venv\Scripts\activate.bat
    echo Please create the virtual environment and install requirements first.
    pause
    exit /b 1
)

REM Start the app using Python module invocation for better compatibility.
python -m streamlit run Bitcoin_pi_top_indicator_UI_main.py

REM Keep this window open so any error/output can be reviewed.
pause
