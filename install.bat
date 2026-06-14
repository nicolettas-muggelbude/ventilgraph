@echo off
title Ventilgraph - Installation

echo === Ventilgraph Installation ===
echo.

:: Python prüfen
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo FEHLER: Python nicht gefunden!
    echo Bitte Python 3.10+ von https://www.python.org/downloads/ installieren.
    echo Beim Installieren "Add Python to PATH" aktivieren.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo Python gefunden: %%v

:: Venv anlegen
if exist ".venv" (
    echo Virtuelle Umgebung bereits vorhanden - Abhaengigkeiten werden aktualisiert...
) else (
    echo Virtuelle Umgebung wird erstellt...
    python -m venv .venv
)

:: Pakete installieren
echo Pakete werden installiert...
.venv\Scripts\pip install --upgrade -q pip
.venv\Scripts\pip install -r requirements.txt

echo.
echo Installation abgeschlossen!
echo Zum Starten: start.bat doppelklicken.
echo.
pause
