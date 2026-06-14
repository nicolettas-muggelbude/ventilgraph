# Ventilgraph

Interaktive Visualisierung von SPS-Prozessdaten einer CIP-Anlage.  
Zoombare Zeitreihen-Darstellung von Ventilzuständen und Analogwerten mit Export-Funktion.

![Ventilgraph Screenshot](assets/screenshot.png)

## Voraussetzungen

- Python 3.10 oder neuer

## Installation & Start

### Linux / macOS

```bash
git clone https://github.com/nicolettas-muggelbude/ventilgraph.git
cd ventilgraph
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Windows

```bat
git clone https://github.com/nicolettas-muggelbude/ventilgraph.git
cd ventilgraph
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Danach im Browser öffnen: **http://localhost:8050**

## CSV-Datei laden

Die App startet mit einer Demo-Datei. Eigene SPS-Exporte lassen sich über den **📂 CSV laden**-Button im Header laden (Drag & Drop oder Dateiauswahl).

**Erwartetes Format:**
- Trennzeichen: `;`
- Dezimalzeichen: `,` (deutsches Format)
- Pflicht-Spalten: `Datum`, `Uhrzeit` (Format `HH:MM:SS.mmm,d`)
- Ventilspalten beginnen mit `Ventil` (Werte 0 oder 1)
- Alle anderen Spalten werden als Analogwerte dargestellt

## Bedienung

| Aktion | Beschreibung |
|--------|-------------|
| Mausrad / Pinch | Zoom auf der Zeitachse |
| Klicken & Ziehen | Zeitausschnitt verschieben |
| Doppelklick | Zoom zurücksetzen |
| 📷 Ausschnitt exportieren | Aktuellen Ausschnitt als PNG speichern |

## Lizenz

MIT License — siehe [LICENSE](LICENSE)
