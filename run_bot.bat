@echo off

cd /d C:\Users\USER\PROJECTS\FOREX_ALERT_BOT

start cmd /k "python scripts/forex_alert.py"

timeout /t 5

start cmd /k "python -m streamlit run scripts/dashboard.py"

pause