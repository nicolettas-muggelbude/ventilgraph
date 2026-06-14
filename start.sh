#!/bin/bash
# Ventilgraph starten (Linux / macOS)
set -e

if [ ! -d ".venv" ]; then
    echo "Virtuelle Umgebung wird erstellt..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Abhängigkeiten prüfen..."
pip install -q -r requirements.txt

echo "App startet auf http://localhost:8050"
python app.py
