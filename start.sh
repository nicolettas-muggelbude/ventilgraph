#!/bin/bash
# Ventilgraph starten (Linux / macOS)
set -e

cd "$(dirname "$0")"

# Läuft der Server bereits? → nur Browser öffnen
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8050/ 2>/dev/null | grep -q "200"; then
    xdg-open http://localhost:8050 2>/dev/null || open http://localhost:8050 2>/dev/null || true
    exit 0
fi

# Venv anlegen falls nicht vorhanden
if [ ! -d ".venv" ]; then
    echo "Ersteinrichtung - bitte kurz warten..."
    python3 -m venv .venv
    .venv/bin/pip install -q -r requirements.txt
fi

# Server im Hintergrund starten
echo "Ventilgraph startet..."
nohup .venv/bin/python app.py > /tmp/ventilgraph.log 2>&1 &

# Warten bis Server antwortet (max. 30 Sekunden)
for i in $(seq 1 30); do
    sleep 1
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8050/ 2>/dev/null | grep -q "200"; then
        xdg-open http://localhost:8050 2>/dev/null || open http://localhost:8050 2>/dev/null || true
        exit 0
    fi
done

echo "Fehler: Server antwortet nicht. Log: /tmp/ventilgraph.log"
exit 1
