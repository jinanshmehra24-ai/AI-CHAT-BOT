@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\activate.bat" (
  echo The toolkit is not installed yet. Double-click install-windows.bat first.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
type HOWTO.txt
cmd /k
