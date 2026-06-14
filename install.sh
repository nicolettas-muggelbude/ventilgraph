#!/bin/bash
# Ventilgraph Installation (Linux / macOS)
set -e

cd "$(dirname "$0")"

echo "=== Ventilgraph Installation ==="
echo

# Python prüfen
if ! command -v python3 &>/dev/null; then
    echo "FEHLER: Python 3 nicht gefunden."
    echo "Ubuntu/Debian: sudo apt install python3 python3-venv"
    echo "macOS:         brew install python"
    exit 1
fi

echo "Python gefunden: $(python3 --version)"

# Venv anlegen
if [ -d ".venv" ]; then
    echo "Virtuelle Umgebung bereits vorhanden - Abhängigkeiten werden aktualisiert..."
else
    echo "Virtuelle Umgebung wird erstellt..."
    python3 -m venv .venv
fi

# pip bootstrappen falls nicht vorhanden (Ubuntu ohne python3-pip)
if [ ! -f ".venv/bin/pip" ]; then
    echo "pip wird nachinstalliert..."
    .venv/bin/python3 -m ensurepip --upgrade
fi

# Pakete installieren
echo "Pakete werden installiert..."
.venv/bin/pip install --upgrade -q pip
.venv/bin/pip install -r requirements.txt

echo
echo "Installation abgeschlossen!"
echo "Zum Starten: ./start.sh"
