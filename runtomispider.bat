@echo off

:: Set the base directory to the script location
set "BASE_DIR=%~dp0"
set "LOG_DIR=%BASE_DIR%ninjacybersquad_tomi\backup\logs"

:: Check if settings file exists
if exist "%BASE_DIR%settings.txt" (
    :: Read settings from the file
    for /f "tokens=1,2 delims==" %%a in (%BASE_DIR%settings.txt) do (
        if /i "%%a"=="open_glogg" (
            set "OPEN_GLOGG=%%b"
        )
    )
)

:: Get today's date in YYYYMMDD format
for /f "tokens=1-3 delims=/. " %%a in ('date /t') do (
    set "TODAY=%%c%%b%%a"
)

:: Define the log file path
set "LOG_FILE=%LOG_DIR%\%TODAY%_log.txt"

:: Check if log directory exists, if not create it
if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
)

:: Open the log file with glogg if the option is set to true in settings.txt
if "%OPEN_GLOGG%"=="true" (
    start "" "C:\Program Files\glogg\glogg.exe" "%LOG_FILE%"
)

:: Run runprocesses.bat and save the output to log.txt with today's date
echo Running runprocesses.bat... (this might take some time)
call "%BASE_DIR%runprocesses.bat" > "%LOG_FILE%" 2>&1

:: Notify when finished
echo Processing finished.

:end
