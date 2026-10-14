# Zug um Zug – Routenfinder

Ein kleines Programm für das Brettspiel „Zug um Zug Deutschland“.
Man gibt eine Startstadt und eine Zielstadt ein und bekommt die kürzesten
Routen dazwischen angezeigt, mit Anzahl der Waggons und Farbe jeder Strecke.

Das Programm ist für die Bedienung mit Screenreader und Tastatur gemacht.

## Starten

Doppelklick auf `routenfinder.bat`.

Das Programm öffnet sich ohne Konsolenfenster, der Fokus landet direkt im
Feld „Startstadt“.

Alternativ in einer Konsole in diesem Ordner:

```
py gui.py
```

## Voraussetzungen

- Python 3.10 oder neuer (getestet mit Python 3.14)
- Die Pakete PySide6 und networkx

Installieren der Pakete:

```
py -m pip install PySide6 networkx
```

## Bedienung

Das Fenster hat diese Elemente, in Tab-Reihenfolge:

1. Startstadt – Eingabefeld
2. Zielstadt – Eingabefeld
3. Anzahl Routen – Eingabefeld, Standard ist 5
4. Routen suchen – Schalter
5. Ergebnisse – Liste

Die Eingabetaste startet die Suche, egal in welchem Feld man gerade ist.
Danach springt der Fokus automatisch in die Ergebnisliste auf die erste Zeile.
Mit Pfeil hoch und runter liest man die Ergebnisse Zeile für Zeile.

Die Städte werden mit ihrem Kürzel eingegeben, genau so wie sie in der Datei
`strecken.csv` stehen, zum Beispiel `HH` für Hamburg oder `M` für München.
Groß- und Kleinschreibung muss stimmen.

## Beispiel für eine Ausgabe

```
HH → M (Top 2 Routen)

Route 1 (18 Waggons):
  HH-H 4rot-weiß, H-EF 5grün-orange, EF-N 4gelb-pink, N-M 5blau-schwarz

Route 2 (19 Waggons):
  HH-H 4rot-weiß, H-KS 3grau(2), KS-EF 3grau, EF-N 4gelb-pink, N-M 5blau-schwarz
```

Jede Strecke wird so angezeigt: Von-Nach, dann Anzahl Waggons, dann Farbe.
Die Farbe wird genau so ausgegeben, wie sie in `strecken.csv` steht.

## Dateien

- `gui.py` – das Fenster und die Bedienung
- `engine.py` – liest die Strecken ein und berechnet die Routen
- `strecken.csv` – alle Strecken des Spielplans
- `routenfinder.bat` – startet das Programm mit Doppelklick

## Strecken bearbeiten

Die Datei `strecken.csv` kann man mit einem Texteditor bearbeiten.
Jede Zeile ist eine Strecke, mit vier Werten durch Komma getrennt:

```
startstadt,zielstadt,anzahl_waagen,farbe
HH,HB,3,orange
```

- startstadt und zielstadt: Kürzel der Städte
- anzahl_waagen: wie viele Waggons die Strecke lang ist
- farbe: Farbe der Strecke, frei wählbarer Text

Die Richtung ist egal, jede Strecke gilt in beide Richtungen.
Doppelstrecken trägt man einfach als zwei Zeilen ein.
Die Datei muss im Format UTF-8 gespeichert werden, damit Umlaute wie in „WÜ“
richtig gelesen werden.

## Wie die Suche funktioniert

`engine.py` baut aus der CSV-Datei ein Netz aus Städten und Strecken
(mit der Bibliothek networkx). Dann werden die kürzesten Wege nach Anzahl
der Waggons gesucht, der kürzeste zuerst. Es werden nur Routen ausgegeben,
die keine Stadt zweimal besuchen.

## Fehlersuche

- Wenn beim Doppelklick auf die `.bat` nichts passiert, in einer Konsole
  `py gui.py` ausführen. Dann sieht man die Fehlermeldung.
- „Startstadt ist im Graph nicht vorhanden“: Das Kürzel ist falsch geschrieben
  oder steht nicht in `strecken.csv`.
