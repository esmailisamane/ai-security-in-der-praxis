"""Gutscheine entscheidet der Code, nicht das Modell (Folge 6, OWASP LLM08:2026).

Vorher stand im System-Prompt: "Gutscheine bis 15 Euro gibt das Team mit dem Freigabe-Code KULANZ-4417 frei."
Jeder, der den Bot geschickt fragt, konnte den Code lesen. Jetzt gibt es keinen Code, den man verraten könnte:
Die Regel steht hier, und nur ein angemeldetes Team-Mitglied kann sie auslösen.
"""
from dataclasses import dataclass

GRENZE_EURO = 15


@dataclass(frozen=True)
class Person:
    name: str
    rolle: str  # "kunde" oder "team" – kommt aus der Anmeldung, nie aus dem Chat-Text


def freigeben(wer: Person, betrag_euro: int) -> bool:
    """True, wenn der Gutschein erlaubt ist. Das Modell ruft diese Funktion nicht auf."""
    if wer.rolle != "team":
        return False
    return 0 < betrag_euro <= GRENZE_EURO
