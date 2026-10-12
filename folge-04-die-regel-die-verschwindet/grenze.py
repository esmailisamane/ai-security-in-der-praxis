"""Wo genau liegt die Grenze? Wir zählen selbst und vergleichen mit Ollama."""
from shopfix import GEDICHT, NUM_CTX, dokument, frage_bot, nachrichten, regel_befolgt, zaehlen

LAEUFE = 10

print(f"Kontextfenster: {NUM_CTX} Tokens\n")
print("Zeilen | wir zählen | laut Ollama | Tokens der Antwort | Regel befolgt")
for zeilen in [220, 221, 222, 223]:
    anfrage = nachrichten(dokument(zeilen) + GEDICHT)
    befolgt = 0
    for seed in range(1, LAEUFE + 1):
        r = frage_bot(anfrage, seed)
        befolgt += regel_befolgt(r.message.content)
    print(f"{zeilen:6d} | {zaehlen(anfrage):10d} | {r.prompt_eval_count:11d} | {r.eval_count:18d} | {befolgt:2d} von {LAEUFE}")
    if zeilen == 222:
        beispiel = r.message.content

print("\nEine Antwort bei 222 Zeilen:")
print(beispiel)
