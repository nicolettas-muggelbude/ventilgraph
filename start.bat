@echo off
REM Ventilgraph starten (Windows)

if not exist ".venv" (
    echo Virtuelle Umgebung wird erstellt...
    python -m venv .venv
)

call .venv\Scripts\activate

echo Abhaengigkeiten pruefen...
pip install -q -r requirements.txt

echo App startet auf http://localhost:8050
python app.py
