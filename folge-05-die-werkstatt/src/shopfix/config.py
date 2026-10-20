"""Einstellungen von ShopFix: Sie kommen aus Umgebungsvariablen, nicht aus dem Code."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Einstellungen:
    modell: str
    num_ctx: int          # Kontextfenster in Tokens (Folge 4)
    antwort_budget: int   # so viel Platz halten wir für die Antwort frei
    temperature: float    # wie stark das Modell würfeln darf

    @property
    def grenze(self):
        """So viele Tokens darf eine Anfrage höchstens haben."""
        return self.num_ctx - self.antwort_budget


def laden():
    """Liest die Einstellungen; ohne Umgebungsvariable gilt der Standardwert."""
    e = Einstellungen(
        modell=os.environ.get("SHOPFIX_MODELL", "llama3.2:3b"),
        num_ctx=int(os.environ.get("SHOPFIX_NUM_CTX", "4096")),
        antwort_budget=int(os.environ.get("SHOPFIX_ANTWORT_BUDGET", "300")),
        temperature=float(os.environ.get("SHOPFIX_TEMPERATURE", "0.7")),
    )
    if e.antwort_budget >= e.num_ctx:
        raise ValueError("Das Antwort-Budget muss kleiner sein als das Kontextfenster.")
    return e
