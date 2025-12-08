@echo off
title TimeTrackerT2 v2.0 - Portable Edition
cls
echo.
echo 🚀 TimeTrackerT2 v2.0 - Avvio Portable
echo =====================================
cd /d "%~dp0"

REM Trova Python
set PYTHON_EXE=
if exist "%~dp0python\python.exe" set PYTHON_EXE=%~dp0python\python.exe
if exist "%~dp0portable_python\python.exe" set PYTHON_EXE=%~dp0portable_python\python.exe
if exist "%~dp0Python39\python.exe" set PYTHON_EXE=%~dp0Python39\python.exe
if exist "%~dp0Python310\python.exe" set PYTHON_EXE=%~dp0Python310\python.exe
if exist "%~dp0Python311\python.exe" set PYTHON_EXE=%~dp0Python311\python.exe
if exist "%~dp0Python312\python.exe" set PYTHON_EXE=%~dp0Python312\python.exe

if "%PYTHON_EXE%"=="" (
    echo 📦 Usando Python di sistema...
    set PYTHON_EXE=python
)

echo ✅ Python: %PYTHON_EXE%
echo 🎯 Avviando TimeTrackerT2 v2.0...
echo.

"%PYTHON_EXE%" main_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Errore nell'avvio dell'applicazione
    echo 🔧 Esegui: python scripts\setup_portable.py
    pause
)
