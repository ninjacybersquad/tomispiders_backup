@echo off
setlocal enabledelayedexpansion

:: Get today's date in YYYYMMDD format
for /f "tokens=1-3 delims=/. " %%a in ('date /t') do (
    set "TODAY=%%c%%b%%a"
)

:: Set the base directory to the script location
set "BASE_DIR=%~dp0"

:: Define backup directories and expected file names
set "BACKUP_DIR=%BASE_DIR%ninjacybersquad_tomi\backup"
set "CRAWLEREXCEL_FILE=!TODAY!_crawled.xlsx"
set "CRAWLERJSON_FILE=!TODAY!_crawled.json"
set "MATCHEDEXCEL_FILE=!TODAY!_matched.xlsx"
set "MATCHEDJSON_FILE=!TODAY!_matched.json"

:: Check for files in backup directories
echo Checking for new files in backup directories...
echo.

:: Navigate to ninjacybersquad_tomi backup directory
cd /d "%BACKUP_DIR%"

:: Check crawlerexcel
if exist "crawlerexcel\!TODAY!_crawled.xlsx" (
    echo Found !TODAY!_crawled.xlsx in crawlerexcel.
) else (
    echo Missing !TODAY!_crawled.xlsx in crawlerexcel.
)

:: Check crawlerjson
if exist "crawlerjson\!TODAY!_crawled.json" (
    echo Found !TODAY!_crawled.json in crawlerjson.
) else (
    echo Missing !TODAY!_crawled.json in crawlerjson.
)

:: Check matchedexcel
if exist "matchedexcel\!TODAY!_matched.xlsx" (
    echo Found !TODAY!_matched.xlsx in matchedexcel.
) else (
    echo Missing !TODAY!_matched.xlsx in matchedexcel.
)

:: Check matchedjson
if exist "matchedjson\!TODAY!_matched.json" (
    echo Found !TODAY!_matched.json in matchedjson.
) else (
    echo Missing !TODAY!_matched.json in matchedjson.
)

endlocal
