"""Zwei Schalter von Ollama: num_keep (Anfang behalten) und truncate (kürzen ja oder nein)."""
import httpx

from shopfix import GEDICHT, MODEL, NUM_CTX, SYSTEM, dokument, frage_bot, nachrichten, regel_befolgt, tokens

LAEUFE = 10
anfrage = nachrichten(dokument(250) + GEDICHT)

# Schalter 1: num_keep = so viele Tokens vom Anfang bleiben bei der Kürzung stehen.
# Start-Token 1 + Kopf 4 + Datumszeile 10 + System-Prompt + Ende-Markierung 1
system_block = 16 + tokens(SYSTEM)
print("num_keep | laut Ollama | Regel befolgt")
for num_keep in [4, system_block]:
    befolgt = 0
    for seed in range(1, LAEUFE + 1):
        r = frage_bot(anfrage, seed, num_keep=num_keep)
        befolgt += regel_befolgt(r.message.content)
    print(f"{num_keep:8d} | {r.prompt_eval_count:11d} | {befolgt:2d} von {LAEUFE}")

# Schalter 2: truncate = false, direkt über die REST-Schnittstelle
# (die Python-Bibliothek 0.6.3 reicht diesen Schalter nicht durch).
antwort = httpx.post(
    "http://localhost:11434/api/chat",
    json={"model": MODEL, "messages": anfrage, "stream": False, "truncate": False,
          "options": {"num_ctx": NUM_CTX, "num_predict": 60}},
    timeout=120,
)
print("\ntruncate=false -> HTTP", antwort.status_code)
print(antwort.text)
