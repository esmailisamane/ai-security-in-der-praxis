"""Längen-Schutz im Code: vor dem Senden zählen, lieber ablehnen als still kürzen, danach nachprüfen."""
from shopfix import GEDICHT, NUM_CTX, dokument, frage_bot, nachrichten, regel_befolgt, zaehlen

LAEUFE = 20
ANTWORT_BUDGET = 300              # Platz im Fenster, den wir für die Antwort freihalten
GRENZE = NUM_CTX - ANTWORT_BUDGET  # so lang darf eine Anfrage höchstens sein
ZU_LANG = "Dein Text ist zu lang für mich. Bitte schick nur den Abschnitt, um den es geht."


class Gekuerzt(Exception):
    """Ollama hat weniger Tokens verarbeitet, als wir geschickt haben."""


def sicherer_bot(text, seed):
    anfrage = nachrichten(text)
    gezaehlt = zaehlen(anfrage)
    if gezaehlt > GRENZE:  # 1) vor dem Senden zählen - zu lang heißt: gar nicht erst senden
        return "abgelehnt", ZU_LANG
    r = frage_bot(anfrage, seed, num_predict=ANTWORT_BUDGET)
    if r.prompt_eval_count != gezaehlt:  # 2) danach nachprüfen: Ist wirklich alles angekommen?
        raise Gekuerzt(f"geschickt: {gezaehlt} Tokens, angekommen: {r.prompt_eval_count}")
    return "ok", r.message.content


print(f"Fenster {NUM_CTX} - Antwort {ANTWORT_BUDGET} = Grenze {GRENZE} Tokens\n")
print("Zeilen | wir zählen | abgelehnt | beantwortet | Regel gebrochen")
for zeilen in [10, 100, 200, 222, 223, 250, 400]:
    text = dokument(zeilen) + GEDICHT
    abgelehnt = gebrochen = 0
    for seed in range(1, LAEUFE + 1):
        status, antwort = sicherer_bot(text, seed)
        abgelehnt += status == "abgelehnt"
        gebrochen += status == "ok" and not regel_befolgt(antwort)
    print(f"{zeilen:6d} | {zaehlen(nachrichten(text)):10d} | {abgelehnt:9d} | {LAEUFE - abgelehnt:11d} "
          f"| {gebrochen} von {LAEUFE}")
