"""Gemeinsame Mess-Schleife für die Versuche dieser Folge: jede Nachricht zehnmal, Quote mit Bereich."""
import json
from pathlib import Path

from shopfix.messen import quote

SEEDS = range(1, 11)


def messen(name, nachrichten, frage, pruefe, details):
    """frage(text, seed) -> Antworttext; pruefe(antwort) -> True, wenn der Angriff geklappt hat."""
    treffer = 0
    for text in nachrichten:
        for seed in SEEDS:
            antwort = frage(text, seed)
            ok = pruefe(antwort)
            treffer += ok
            details.append({"versuch": name, "nachricht": text, "seed": seed, "erfolg": ok, "antwort": antwort[:400]})
    n = len(nachrichten) * len(SEEDS)
    print(f"{name:28s} | {quote(treffer, n)}", flush=True)
    return treffer, n


def speichern(datei, daten):
    ziel = Path("outputs") / datei
    ziel.write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nGespeichert: {ziel.as_posix()}")
