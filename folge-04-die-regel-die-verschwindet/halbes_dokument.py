"""Nicht nur die Regel fehlt: Auch vom Dokument kommt nur die hintere Hälfte an."""
from shopfix import ZEILE, dokument, frage_bot, nachrichten

LAEUFE = 10
AUSNAHME = "Abschnitt 7: Reduzierte Ware ist von der Rücksendung ausgeschlossen.\n"
FRAGE = "\nKann ich reduzierte Ware zurückschicken? Antworte mit Ja oder Nein und nenne den Abschnitt."

print("Zeilen | Tokens laut Ollama | richtig (Nein) | eine Antwort")
for zeilen in [100, 250]:
    text = dokument(zeilen).replace(ZEILE.format(i=7), AUSNAHME) + FRAGE  # die Ausnahme steht weit vorn
    richtig = 0
    for seed in range(1, LAEUFE + 1):
        r = frage_bot(nachrichten(text), seed)
        antwort = r.message.content.replace("\n", " ")
        richtig += antwort.strip().lower().startswith("nein")
    print(f"{zeilen:6d} | {r.prompt_eval_count:18d} | {richtig:2d} von {LAEUFE}      | {antwort[:70]}")
