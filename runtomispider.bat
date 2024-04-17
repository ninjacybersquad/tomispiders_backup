@echo off

:: Get today's date in YYYYMMDD format
for /f "tokens=1-3 delims=/. " %%a in ('date /t') do (
    set "TODAY=%%c%%b%%a"
)

:: Set the base directory to the script location
set "BASE_DIR=%~dp0"

:: Run runprocesses.bat and save the output to log.txt with today's date
echo Running runprocesses.bat... (this might take some time)
call "%BASE_DIR%runprocesses.bat" > "%BASE_DIR%ninjacybersquad_tomi\backup\logs\%TODAY%_log.txt" 2>&1

:: Notify when finished
echo Processing finished.

:end
