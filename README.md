# Zug um Zug – Streckenfinder

Ein kleines Programm für das Brettspiel „Zug um Zug Deutschland“.
Du gibst eine Startstadt und eine Zielstadt ein und bekommst die kürzesten
Routen dazwischen angezeigt, mit Anzahl der Waggons und Farbe jeder Strecke.

Das Programm ist für die Bedienung mit Screenreader und Tastatur gemacht.

## Warum es dieses Programm gibt

Im Spiel musst du wissen, welche Farben du sammeln solltest, um deine
Streckenkarten zu erfüllen. Die anderen sollen aber nicht merken, wo du
bauen willst. Spielen nur Blinde unter sich, ist das kein großes Problem.
Mit Sehenden wird es schwierig, wenn du lange auf dem Spielplan nach
Verbindungen tastest. Mit dem Streckenfinder findest du deine Route
unauffällig am Laptop und weißt sofort, wie viele Karten in welchen
Farben du brauchst.

Wie ich Zug um Zug für Blinde barrierefrei gemacht habe, mit Klett oder
mit Magneten, beschreibe ich auf meinem Blog
[Blind Move](https://blindmoveblog.wordpress.com/).
Dort gibt es auch viele weitere Gesellschaftsspiele, die blind spielbar sind.

## Download

Es gibt eine Exe für Windows. Du musst nichts installieren.

1. Lade die ZIP-Datei unter [Releases](../../releases/latest) herunter.
2. Entpacke die ZIP-Datei in einen Ordner deiner Wahl.
3. Starte `Zug-um-Zug-Streckenfinder.exe` mit Doppelklick oder Enter.

Neben der Exe liegt die Datei `strecken.csv` mit allen Strecken des Spielplans.
Das Programm liest diese Datei beim Start ein. Fehlt sie, verwendet es die
Strecken, die in die Exe eingebaut sind.

## Windows-Warnung

Windows zeigt beim ersten Start vielleicht „Der Computer wurde durch Windows
geschützt“, weil die Exe nicht signiert ist. Wähle dann „Weitere Informationen“
und danach „Trotzdem ausführen“.

## Bedienung

Das Fenster hat diese Elemente, in Tab-Reihenfolge:

1. Startstadt – Eingabefeld
2. Zielstadt – Eingabefeld
3. Anzahl Routen – Eingabefeld, Standard ist 5
4. Routen suchen – Schalter
5. Ergebnisse – Liste

Beim Start landet der Fokus direkt im Feld „Startstadt“.
Die Eingabetaste startet die Suche, egal in welchem Feld du gerade bist.
Danach springt der Fokus automatisch in die Ergebnisliste auf die erste Zeile.
Mit Pfeil hoch und runter liest du die Ergebnisse Zeile für Zeile.

Die Städte gibst du mit ihrem Kürzel ein, zum Beispiel `HH` für Hamburg oder
`M` für München. Groß- und Kleinschreibung muss stimmen.
Alle Kürzel findest du weiter unten in der Liste der Städtekürzel.

## Beispiel für eine Ausgabe

```
HH → M (Top 2 Routen)

Route 1 (18 Waggons):
  HH-H 4rot-weiß, H-EF 5grün-orange, EF-N 4gelb-pink, N-M 5blau-schwarz

Route 2 (19 Waggons):
  HH-H 4rot-weiß, H-KS 3grau(2), KS-EF 3grau, EF-N 4gelb-pink, N-M 5blau-schwarz
```

Jede Strecke wird so angezeigt: Von-Nach, dann Anzahl Waggons, dann Farbe.

- Zwei Farben mit Bindestrich, zum Beispiel `rot-weiß`, bedeuten eine
  Doppelstrecke: Du kannst eine der beiden Farben bauen.
- `grau` bedeutet: Du kannst die Strecke mit Karten in einer beliebigen Farbe
  bauen, alle Karten müssen aber dieselbe Farbe haben.
- `grau(2)` bedeutet: Es gibt zwei graue Strecken nebeneinander.

## Städtekürzel

Die Kürzel sind die Kfz-Kennzeichen der Städte. Die Nachbarländer haben ihr
Länderkürzel. So habe ich auch meinen taktilen Spielplan und die
Streckenkarten beschriftet.

### Städte

- A: Augsburg
- B: Berlin
- C: Chemnitz
- D: Düsseldorf
- DD: Dresden
- DO: Dortmund
- EF: Erfurt
- EMD: Emden
- F: Frankfurt
- FR: Freiburg
- H: Hannover
- HB: Bremen
- HBV: Bremerhaven
- HH: Hamburg
- HRO: Rostock
- K: Köln
- KA: Karlsruhe
- KI: Kiel
- KN: Konstanz
- KO: Koblenz
- KS: Kassel
- L: Leipzig
- LI: Lindau
- M: München
- MA: Mannheim
- MD: Magdeburg
- MS: Münster
- MZ: Mainz
- N: Nürnberg
- R: Regensburg
- S: Stuttgart
- SB: Saarbrücken
- SN: Schwerin
- UL: Ulm
- WÜ: Würzburg

### Länder

- AUT: Österreich
- CHE: Schweiz
- DNK: Dänemark
- FRA: Frankreich
- NLD: Niederlande

## Strecken bearbeiten

Du kannst die Strecken selbst anpassen, zum Beispiel für eine andere Version
von Zug um Zug. Dafür musst du nichts neu bauen: Bearbeite einfach die Datei
`strecken.csv` neben der Exe mit einem Texteditor und starte das Programm neu.
Jede Zeile ist eine Strecke, mit vier Werten durch Komma getrennt:

```
startstadt,zielstadt,anzahl_waagen,farbe
HH,HB,3,orange
```

- startstadt und zielstadt: Kürzel der Städte
- anzahl_waagen: wie viele Waggons die Strecke lang ist
- farbe: Farbe der Strecke, frei wählbarer Text

Die Richtung ist egal, jede Strecke gilt in beide Richtungen.
Doppelstrecken trägst du einfach als zwei Zeilen ein.
Die Datei muss im Format UTF-8 gespeichert werden, damit Umlaute wie in „WÜ“
richtig gelesen werden.

## Fehlersuche

- „Startstadt ist im Graph nicht vorhanden“: Das Kürzel ist falsch geschrieben
  oder steht nicht in `strecken.csv`. Achte auf Groß- und Kleinschreibung.
- Nach einer Änderung an `strecken.csv` stimmt etwas nicht: Prüfe, ob jede
  Zeile genau vier Werte hat und die Datei als UTF-8 gespeichert ist.

## Für Entwickler: Start aus dem Quellcode

Du brauchst Python 3.10 oder neuer (getestet mit Python 3.14) und die Pakete
PySide6 und networkx:

```
py -m pip install PySide6 networkx
```

Dann startest du das Programm mit Doppelklick auf `routenfinder.bat` oder in
einer Konsole in diesem Ordner mit:

```
py gui.py
```

Wenn beim Doppelklick auf die `.bat` nichts passiert, führe `py gui.py` in
einer Konsole aus. Dann siehst du die Fehlermeldung.

### Dateien

- `gui.py` – das Fenster und die Bedienung
- `engine.py` – liest die Strecken ein und berechnet die Routen
- `strecken.csv` – alle Strecken des Spielplans
- `routenfinder.bat` – startet das Programm mit Doppelklick

### Wie die Suche funktioniert

`engine.py` baut aus der CSV-Datei ein Netz aus Städten und Strecken
(mit der Bibliothek networkx). Dann werden die kürzesten Wege nach Anzahl
der Waggons gesucht, der kürzeste zuerst. Es werden nur Routen ausgegeben,
die keine Stadt zweimal besuchen.

## Lizenz

Lizenz: MIT. Der vollständige Text steht in [LICENSE](LICENSE).
