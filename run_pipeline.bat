@echo off
title Sales Data Analysis - Pipeline Runner
cd /d "%~dp0"

echo =========================================================
echo    Sales Data Analysis - End-to-End Pipeline Runner
echo =========================================================
echo.

python src\run_all.py

echo.
echo Press any key to exit...
pause >nul
