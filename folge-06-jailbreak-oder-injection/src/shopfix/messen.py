"""Richtig messen: eine Quote ist erst mit ihrem Unsicherheitsbereich eine Aussage."""
import math


def wilson(treffer, n, z=1.96):
    """95-%-Bereich für eine Quote (Wilson-Intervall) – funktioniert auch bei 0 oder n Treffern."""
    if n == 0:
        return 0.0, 1.0
    p = treffer / n
    nenner = 1 + z * z / n
    mitte = (p + z * z / (2 * n)) / nenner
    breite = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / nenner
    return max(0.0, mitte - breite), min(1.0, mitte + breite)


def quote(treffer, n):
    """Zum Lesen: '96 von 100 = 96 % (95 %-Bereich: 90 % bis 98 %)'."""
    unten, oben = wilson(treffer, n)
    return f"{treffer} von {n} = {prozent(treffer / n)} (95 %-Bereich: {prozent(unten)} bis {prozent(oben)})"


def prozent(x):
    return f"{round(x * 100)} %"


def wiederholen(pruefung, seeds):
    """Führt pruefung(seed) für jeden Seed aus und zählt, wie oft sie True ergibt."""
    return sum(bool(pruefung(seed)) for seed in seeds)
