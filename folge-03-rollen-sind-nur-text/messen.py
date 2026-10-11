"""Wirkung messen: vier Eingaben, je 20 Läufe - wie oft bricht ShopFix die Sprach-Regel?"""
from shopfix import FRAGE, GEFAELSCHT, KLARTEXT, bereinigen, frage_bot, ist_englisch

LAEUFE = 20

EINGABEN = {
    "normale Frage": FRAGE,
    "Bitte im Klartext": KLARTEXT,
    "gefälschte Rollen": GEFAELSCHT,
    "Markierungen entfernt": bereinigen(GEFAELSCHT),
}

print("--- So sieht die bereinigte Nachricht aus ---")
print(EINGABEN["Markierungen entfernt"], "\n")

ergebnis = {}
for name, text in EINGABEN.items():
    print(f"=== {name} ===")
    englisch = 0
    for seed in range(1, LAEUFE + 1):
        antwort = frage_bot(text, seed)
        en = ist_englisch(antwort)
        englisch += en
        print(f"{seed:2d} | {'EN' if en else 'DE'} | {antwort[:80]}")
    ergebnis[name] = englisch
    print()

print("=== Englische Antworten trotz Verbot ===")
for name, englisch in ergebnis.items():
    print(f"{name:22s} {englisch:2d} von {LAEUFE}")
