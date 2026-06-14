@echo off
setlocal enabledelayedexpansion
title Ventilgraph

:: Python prüfen
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python nicht gefunden!
    echo Bitte Python 3.10+ von https://www.python.org/downloads/ installieren.
    echo Beim Installieren "Add Python to PATH" aktivieren.
    pause
    exit /b 1
)

:: Läuft der Server bereits? → nur Browser öffnen
powershell -Command "try{(Invoke-WebRequest http://localhost:8050/ -UseBasicParsing -TimeoutSec 1).StatusCode}catch{0}" | find "200" >nul 2>&1
if %errorlevel%==0 (
    start http://localhost:8050
    exit /b 0
)

:: Venv anlegen falls nicht vorhanden
if not exist ".venv" (
    echo Ersteinrichtung - bitte kurz warten...
    python -m venv .venv
    .venv\Scripts\pip install -q -r requirements.txt
)

:: Server minimiert starten
start /min "Ventilgraph" .venv\Scripts\python app.py

:: Warten bis Server antwortet (max. 30 Sekunden)
set /a i=0
:wait
    set /a i+=1
    if !i! gtr 30 (
        echo Fehler: Server antwortet nicht. Bitte Fenster in der Taskleiste pruefen.
        pause
        exit /b 1
    )
    timeout /t 1 /nobreak >nul
    powershell -Command "try{(Invoke-WebRequest http://localhost:8050/ -UseBasicParsing -TimeoutSec 1).StatusCode}catch{0}" | find "200" >nul 2>&1
if not %errorlevel%==0 goto wait

start http://localhost:8050
