import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QShortcut, QKeySequence

from engine import build_graph_from_csv, find_routes_text


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zug um Zug – Routenfinder")

        # Graph einmal laden
        try:
            self.G = build_graph_from_csv()   # strecken.csv neben der EXE, sonst eingebaut
            self.startup_error = None
        except Exception as e:
            self.G = None
            self.startup_error = str(e)

        # --- Eingaben ---
        self.lbl_start = QLabel("Startstadt")
        self.inp_start = QLineEdit()
        self.inp_start.setText("")
        self.inp_start.setAccessibleName("Startstadt")

        self.lbl_ziel = QLabel("Zielstadt")
        self.inp_ziel = QLineEdit()
        self.inp_ziel.setText("")
        self.inp_ziel.setAccessibleName("Zielstadt")

        self.lbl_anzahl = QLabel("Anzahl Routen")
        self.inp_anzahl = QLineEdit()
        self.inp_anzahl.setText("5")
        self.inp_anzahl.setAccessibleName("Anzahl Routen")

        # --- Button: Routen suchen ---
        self.btn_search = QPushButton("Routen suchen")
        self.btn_search.setAccessibleName("Routen suchen")
        self.btn_search.clicked.connect(self.on_search)

        # Default-Button: Enter löst Suche aus
        self.btn_search.setAutoDefault(True)
        self.btn_search.setDefault(True)

        # Enter in Eingabefeldern startet Suche
        self.inp_start.returnPressed.connect(self.on_search)
        self.inp_ziel.returnPressed.connect(self.on_search)
        self.inp_anzahl.returnPressed.connect(self.on_search)

        # Global: Enter startet Suche (robust)
        QShortcut(QKeySequence("Return"), self, activated=self.on_search)
        QShortcut(QKeySequence("Enter"), self, activated=self.on_search)  # Numpad-Enter

        # --- Ausgabe als Liste ---
        self.lbl_out = QLabel("Ausgabe")
        self.out = QListWidget()
        self.out.setAccessibleName("Ergebnisse")

        # --- Layout (Reihenfolge: Start, Ziel, Anzahl, Suchen, Ausgabe) ---
        layout = QGridLayout()

        layout.addWidget(self.lbl_start, 0, 0)
        layout.addWidget(self.inp_start, 0, 1)

        layout.addWidget(self.lbl_ziel, 1, 0)
        layout.addWidget(self.inp_ziel, 1, 1)

        layout.addWidget(self.lbl_anzahl, 2, 0)
        layout.addWidget(self.inp_anzahl, 2, 1)

        layout.addWidget(self.btn_search, 3, 1)

        layout.addWidget(self.lbl_out, 4, 0, Qt.AlignTop)
        layout.addWidget(self.out, 4, 1)

        # Ausgabe soll Platz bekommen
        layout.setColumnStretch(1, 1)
        layout.setRowStretch(4, 1)

        self.setLayout(layout)

        # --- Tab-Reihenfolge explizit ---
        QWidget.setTabOrder(self.inp_start, self.inp_ziel)
        QWidget.setTabOrder(self.inp_ziel, self.inp_anzahl)
        QWidget.setTabOrder(self.inp_anzahl, self.btn_search)
        QWidget.setTabOrder(self.btn_search, self.out)

        # Startfokus
        self.inp_start.setFocus()

        # Startup-Fehler anzeigen
        if self.startup_error:
            self.out.addItem(QListWidgetItem("Fehler beim Laden der CSV:"))
            self.out.addItem(QListWidgetItem(self.startup_error))

    def on_search(self):
        if self.G is None:
            QMessageBox.critical(self, "Fehler", f"CSV/Graph nicht geladen:\n{self.startup_error}")
            return

        start = self.inp_start.text().strip()
        ziel = self.inp_ziel.text().strip()
        anzahl_text = self.inp_anzahl.text().strip()

        if not start or not ziel:
            QMessageBox.warning(self, "Eingabefehler", "Bitte Startstadt und Zielstadt ausfüllen.")
            return

        try:
            anzahl = int(anzahl_text)
            if anzahl <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Eingabefehler", "Anzahl Routen muss eine positive ganze Zahl sein.")
            return

        result = find_routes_text(self.G, start, ziel, anzahl)

        # Liste neu füllen: jede Zeile als eigenes Element
        self.out.clear()
        for line in result.splitlines():
            self.out.addItem(QListWidgetItem(line if line else " "))

        # Fokus in die Liste + erstes Element auswählen
        if self.out.count() > 0:
            self.out.setCurrentRow(0)
        self.out.setFocus()


def fenster_in_vordergrund(w):
    """Holt das Fenster nach vorne und gibt ihm den Tastaturfokus.

    Windows verhindert normalerweise, dass ein neu gestartetes Programm
    sich selbst in den Vordergrund holt (z. B. wenn es über eine .bat
    gestartet wird). Mit AttachThreadInput an den aktuellen
    Vordergrund-Thread klappt es trotzdem.
    """
    w.raise_()
    w.activateWindow()

    if sys.platform != "win32":
        return

    import ctypes
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    hwnd = int(w.winId())
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    eigener_thread = kernel32.GetCurrentThreadId()

    if fg_thread and fg_thread != eigener_thread:
        user32.AttachThreadInput(fg_thread, eigener_thread, True)
        user32.BringWindowToTop(hwnd)
        user32.SetForegroundWindow(hwnd)
        user32.AttachThreadInput(fg_thread, eigener_thread, False)
    else:
        user32.SetForegroundWindow(hwnd)

    w.activateWindow()
    w.inp_start.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(780, 420)  # optional
    w.show()
    # erst nach dem Anzeigen ausführen, wenn das Fenster wirklich existiert
    QTimer.singleShot(100, lambda: fenster_in_vordergrund(w))
    sys.exit(app.exec())
