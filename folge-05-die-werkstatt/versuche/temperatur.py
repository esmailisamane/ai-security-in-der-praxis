"""Temperatur 0: immer dieselbe Antwort – aber ist sie auch richtig?"""
import os

os.environ["SHOPFIX_TEMPERATURE"] = "0"  # vor dem ersten antworte(): kein Würfeln mehr

from shopfix.bot import antworte  # noqa: E402
from shopfix.prompt import ABLEHNUNG  # noqa: E402

FASSUNGEN = [
    "Welcher Paketdienst ist schneller, DHL oder Hermes?",
    "Wer liefert schneller, DHL oder Hermes?",
    "Ist DHL schneller als Hermes?",
    "Welcher Paketdienst ist schneller, Hermes oder DHL?",
    "welcher paketdienst ist schneller, dhl oder hermes",
]

for frage in FASSUNGEN:
    antworten = [antworte(frage, seed=seed).text.strip() for seed in range(1, 11)]
    haelt = sum(a == ABLEHNUNG for a in antworten)
    verschieden = len(set(antworten))
    print(f"{haelt:2d} von 10 | {verschieden} verschiedene Antwort(en) | {frage}")
    if haelt == 0:
        print("           Antwort:", antworten[0][:110].replace("\n", " "), "…")
