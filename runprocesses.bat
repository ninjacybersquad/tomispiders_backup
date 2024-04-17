@echo off
setlocal enabledelayedexpansion

:: Run Scrapy crawl in the Spider directory
echo Running Scrapy crawl...
cd /d "%~dp0\ninjacybersquad_tomi\zweispurigSpider"
scrapy crawl zweispurig

:: Run comparer Python script in the Comparer directory
echo Running comparer script...
cd /d "%~dp0\ninjacybersquad_tomi\comparespiders"
python comparethem.py

:: Run checkfiles.bat
echo Running checkfiles.bat...
call "%~dp0\checkfiles.bat"

:end
endlocal
