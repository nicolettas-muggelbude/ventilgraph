# Ventilgraph

Interaktive Visualisierung von SPS-Prozessdaten einer CIP-Anlage.  
Ventilzustände als Gantt-Balken, Analogwerte (Temperatur, Leitfähigkeit, Füllstände) als Liniendiagramm — zoombar und exportierbar.

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

## Updates einspielen

```bash
git pull
./start.sh   # bzw. start.bat — startet den Server automatisch neu
```

Der laufende Server wird beim Start automatisch beendet, neue Version wird sofort aktiv.

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

## Analysefokus

Unterhalb des Headers befinden sich zwei Dropdowns:

- **Ventile** — welche Ventile im oberen Panel angezeigt werden
- **Analogwerte** — welche Messwerte im unteren Graphen angezeigt werden

Einfach gewünschte Signale auswählen, der Graph aktualisiert sich sofort.  
Beispiel: nur *Leitfähigkeit* + *Ventil Wasser* + *Ventil Gully* — so ist auf einen Blick erkennbar, wann der Leitwert fällt und welches Ventil dafür verantwortlich ist.

## Lizenz

MIT License — siehe [LICENSE](LICENSE)
