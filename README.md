# Ventilgraph

Interaktive Visualisierung von SPS-Prozessdaten einer CIP-Anlage.  
Zoombare Zeitreihen-Darstellung von Ventilzuständen und Analogwerten mit Export-Funktion.

![Ventilgraph Screenshot](assets/screenshot.png)

## Voraussetzungen

- Python 3.10 oder neuer → [python.org/downloads](https://www.python.org/downloads/)  
  ⚠️ Beim Installieren **"Add Python to PATH"** aktivieren

## Installation & Start

### Windows

**Einmalig bei der ersten Einrichtung:**
1. Repo herunterladen: grüner **Code**-Button → **Download ZIP** → entpacken  
   *(oder `git clone https://github.com/nicolettas-muggelbude/ventilgraph.git`)*
2. `install.bat` doppelklicken — installiert alle Abhängigkeiten (~1 Minute)

**Täglich:**
- `start.bat` doppelklicken → Browser öffnet sich automatisch

### Linux / macOS

**Einmalig:**
```bash
git clone https://github.com/nicolettas-muggelbude/ventilgraph.git
cd ventilgraph
chmod +x install.sh start.sh
./install.sh
```

**Täglich:**
```bash
./start.sh
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
