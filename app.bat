@echo off
call _internal\setenv.bat

"%PYTHON_EXECUTABLE%" "%APP_ROOT%\main.py"

pause