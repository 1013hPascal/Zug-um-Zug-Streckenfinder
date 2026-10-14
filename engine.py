import csv
import sys
from pathlib import Path
from itertools import islice

import networkx as nx


def resource_path(rel_path: str) -> Path:
    """
    Liefert den korrekten Pfad zu Dateien, die mit PyInstaller gebundelt werden.
    - normal: relativ zu dieser Datei (engine.py)
    - PyInstaller onefile: relativ zu sys._MEIPASS (Temp-Ordner)
    """
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / rel_path


def add_track(G, u, v, length, color, track_id):
    """
    DiGraph: wir legen die Strecke in beide Richtungen an.
    So funktioniert Start->Ziel und Ziel->Start gleichermaßen.
    """
    e_uv = f"EDGE:{u}-{v}:{track_id}"
    G.add_edge(u, e_uv, weight=length, length=length, color=color, kind="track")
    G.add_edge(e_uv, v, weight=0, kind="link")

    e_vu = f"EDGE:{v}-{u}:{track_id}"
    G.add_edge(v, e_vu, weight=length, length=length, color=color, kind="track")
    G.add_edge(e_vu, u, weight=0, kind="link")


def is_edge_node(n):
    return isinstance(n, str) and n.startswith("EDGE:")


def path_to_segments(G, path):
    pretty = []
    total = 0

    # Wir suchen immer die Schritte Stadt -> EDGE -> Stadt
    for i in range(0, len(path) - 2):
        a = path[i]
        b = path[i + 1]
        c = path[i + 2]

        if not is_edge_node(b):
            continue

        data = G.get_edge_data(a, b)
        if not data or data.get("kind") != "track":
            continue

        length = data["length"]
        color = data["color"]

        pretty.append(f"{a}-{c} {length}{color}")
        total += length

    return pretty, total


def build_graph_from_csv(csv_datei: str | None = None) -> nx.DiGraph:
    """
    CSV wird 1x eingelesen, Graph wird gebaut und zurückgegeben.

    Wenn csv_datei None ist, wird automatisch 'strecken.csv' geladen
    (funktioniert normal + in PyInstaller onefile EXE).
    """
    csv_path = Path(csv_datei) if csv_datei else resource_path("strecken.csv")

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV-Datei nicht gefunden: {csv_path}")

    G = nx.DiGraph()
    track_counter = {}

    with csv_path.open(mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {"startstadt", "zielstadt", "anzahl_waagen", "farbe"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"CSV braucht Spalten: {sorted(required)}")

        for row in reader:
            u = row["startstadt"].strip()
            v = row["zielstadt"].strip()
            length = int(row["anzahl_waagen"])
            color = row["farbe"].strip()

            key = tuple(sorted([u, v]))
            track_id = track_counter.get(key, 0)
            track_counter[key] = track_id + 1

            add_track(G, u, v, length, color, track_id)

    return G


def find_routes_text(G: nx.DiGraph, startstadt: str, zielstadt: str, anzahl_routen: int) -> str:
    """
    Berechnet Top-k Routen und gibt einen gut lesbaren Text zurück.
    """
    startstadt = startstadt.strip()
    zielstadt = zielstadt.strip()

    if startstadt not in G:
        return f"Fehler: Startstadt '{startstadt}' ist im Graph nicht vorhanden."
    if zielstadt not in G:
        return f"Fehler: Zielstadt '{zielstadt}' ist im Graph nicht vorhanden."

    try:
        paths_iter = nx.shortest_simple_paths(G, startstadt, zielstadt, weight="weight")
        paths = list(islice(paths_iter, anzahl_routen))
    except nx.NetworkXNoPath:
        return f"Keine Route gefunden von {startstadt} nach {zielstadt}."

    lines = [f"{startstadt} → {zielstadt} (Top {anzahl_routen} Routen)", ""]

    for i, p in enumerate(paths, start=1):
        segments, total = path_to_segments(G, p)
        lines.append(f"Route {i} ({total} Waggons):")
        lines.append("  " + ", ".join(segments))
        lines.append("")

    return "\n".join(lines)
