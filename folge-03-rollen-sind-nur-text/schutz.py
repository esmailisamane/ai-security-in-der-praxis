"""Schutz im Code: Eingabe prüfen (ablehnen statt bereinigen) und Ausgabe prüfen."""
from shopfix import FRAGE, GEFAELSCHT, KLARTEXT, MARKER, bereinigen, frage_bot, ist_englisch

LAEUFE = 20
ABLEHNUNG = "Deine Nachricht enthält Zeichenfolgen, die wir nicht verarbeiten. Bitte formuliere sie neu."
ERSATZ = "Das kann ich gerade nicht beantworten. Unser Support-Team meldet sich bei dir."


def sicherer_bot(text, seed):
    """Zwei Prüfungen im Code - das Modell entscheidet hier nichts."""
    if MARKER.search(text):  # 1) Kein Kunde tippt <|...|> aus Versehen: gar nicht erst senden
        return "abgelehnt", ABLEHNUNG
    antwort = frage_bot(text, seed)
    if ist_englisch(antwort):  # 2) Die Regel "nur Deutsch" prüft der Code, nicht der Prompt
        return "ersetzt", ERSATZ
    return "ok", antwort


EINGABEN = {
    "normale Frage": FRAGE,
    "Bitte im Klartext": KLARTEXT,
    "gefälschte Rollen": GEFAELSCHT,
    "Markierungen entfernt": bereinigen(GEFAELSCHT),
}

print(f"{'Eingabe':22s} | abgelehnt | ersetzt | ok | Englisch beim Kunden")
for name, text in EINGABEN.items():
    zaehler = {"abgelehnt": 0, "ersetzt": 0, "ok": 0}
    englisch = 0
    for seed in range(1, LAEUFE + 1):
        status, antwort = sicherer_bot(text, seed)
        zaehler[status] += 1
        englisch += ist_englisch(antwort)
    print(f"{name:22s} | {zaehler['abgelehnt']:9d} | {zaehler['ersetzt']:7d} | {zaehler['ok']:2d} | {englisch} von {LAEUFE}")
