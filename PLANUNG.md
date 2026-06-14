# Ventilgraph – Projektplan

## Ziel
Interaktive Visualisierung von SPS-Prozessdaten einer CIP-Anlage (Brauerei).
Zoombare Zeitreihen-Darstellung mit Export-Funktion für Ausschnitte.

## Datenbasis
- `CIP1_10s.csv` — 10-Sekunden-Takt (~10.000 Zeilen) ← Entwicklung/Test
- `CIP1_1s.csv`  — 1-Sekunden-Takt (~100.000 Zeilen)
- `CIP1.csv`     — 144 Hz (~1.000.000 Zeilen, für spätere Optimierung)

### CSV-Details (noch ausstehend)
- Trennzeichen: ? (Semikolon oder Komma)
- Dezimalzeichen: ? (Komma oder Punkt)
- Spaltennamen (bekannt aus Screenshot):
  - `Uhrzeit` — Zeitstempel
  - `Ventil P1 CII` bis `Ventil P13 C` — Binäre Schaltzustände (0/1)
  - `Leitfähigkeit`
  - `Temperatur` (mehrere Spalten)
  - `Niveau Säure` (mehrere Spalten)
  - `Niveau Lauge` (mehrere Spalten)

## Technologie-Stack
- **Python** (pandas, plotly, dash)
- **Dash** — lokale Web-App, läuft im Browser
- **Plotly** — interaktive Grafiken (zoom, pan, hover)
- **kaleido** — PNG/SVG-Export des aktuellen Ausschnitts

## Darstellung (2-Panel-Layout)
```
┌─────────────────────────────────────────────┐
│ Ventil P1  ████████░░░░░████████░░░░░░░░░░░ │  ← farbige Gantt-Balken
│ Ventil P2  ░░░░░░░░████████░░░░░████████░░░ │
│ ...                                          │
├─────────────────────────────────────────────┤
│ Leitfähigkeit ~~~~~~~~~~~~~~~~~~~~~         │  ← Linienkurven
│ Temperatur 1  ~~~~~~~~~~~~~~~~~~~~~         │
│ Niveau Säure  ~~~~~~~~~~~~~~~~~~~~~         │
└─────────────────────────────────────────────┘
       [📷 Ausschnitt exportieren]
```
- Beide Panels zoomen synchron (shared x-axis)
- Hover zeigt Zeitstempel + Wert
- Export-Button speichert aktuellen Ausschnitt als PNG

## Geplante Dateistruktur
```
ventilgraph/
├── PLANUNG.md          ← diese Datei
├── requirements.txt
├── app.py              ← Dash-App (Hauptdatei)
├── data_loader.py      ← CSV-Ladelogik mit pandas
├── charts.py           ← Plotly-Figuren (Ventile + Analog)
└── data/               ← CSV-Dateien hier ablegen
```

## Offene Fragen / nächste Schritte
1. [ ] CSV-Rohzeilen (erste 3-4 Zeilen) für genaue Spaltennamen + Trennzeichen
2. [ ] Code schreiben (data_loader, charts, app)
3. [ ] Test mit CIP1_10s.csv
4. [ ] Performance-Test mit 1s-Datei
5. [ ] Ggf. Downsampling für 144Hz-Datei (LTTB-Algorithmus)
