"""Der Kunde fügt einen immer längeren Text ein. Hält die Regel?"""
from shopfix import GEDICHT, dokument, frage_bot, nachrichten, regel_befolgt

LAEUFE = 20

print("Zeilen | Tokens laut Ollama | Regel befolgt | eine Antwort")
for zeilen in [10, 100, 200, 250, 400]:
    text = dokument(zeilen) + GEDICHT
    befolgt = 0
    for seed in range(1, LAEUFE + 1):
        r = frage_bot(nachrichten(text), seed)
        befolgt += regel_befolgt(r.message.content)
    antwort = r.message.content.replace("\n", " ")
    print(f"{zeilen:6d} | {r.prompt_eval_count:18d} | {befolgt:2d} von {LAEUFE}     | {antwort[:45]}")
