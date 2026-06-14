@echo off
setlocal enabledelayedexpansion
title Ventilgraph

:: Läuft der Server bereits?
powershell -Command "try{(Invoke-WebRequest http://localhost:8050/ -UseBasicParsing -TimeoutSec 1).StatusCode}catch{0}" | find "200" >nul 2>&1
if %errorlevel%==0 (
    echo Server laeuft bereits - Browser wird geoeffnet.
    start http://localhost:8050
    exit /b 0
)

echo Ventilgraph startet...
start /min "Ventilgraph" wsl -d Ubuntu-24.04 -- bash -c "cd /home/nicole/projekte/ventilgraph && .venv/bin/python app.py"

:: Warten bis Server antwortet (max. 30 Sekunden)
set /a i=0
:wait
    set /a i+=1
    if !i! gtr 30 (
        echo FEHLER: Server antwortet nicht. Fenster pruefen.
        pause
        exit /b 1
    )
    timeout /t 1 /nobreak >nul
    powershell -Command "try{(Invoke-WebRequest http://localhost:8050/ -UseBasicParsing -TimeoutSec 1).StatusCode}catch{0}" | find "200" >nul 2>&1
if not %errorlevel%==0 goto wait

start http://localhost:8050
