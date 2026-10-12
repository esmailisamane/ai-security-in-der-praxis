"""Ein langes Gespräch statt eines langen Textes: Was wirft Ollama hier weg?"""
from shopfix import GEDICHT, SYSTEM, frage_bot, regel_befolgt, zaehlen

LAEUFE = 5
NUMMER = "48213"


def gespraech(runden, letzte_frage):
    """Der Kunde nennt am Anfang seine Bestellnummer, dann folgen viele Fragen und Antworten."""
    verlauf = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Hallo, meine Bestellnummer ist {NUMMER}."},
        {"role": "assistant", "content": "Danke, ich habe die Bestellnummer notiert."},
    ]
    for i in range(1, runden + 1):
        verlauf.append({"role": "user", "content": f"Kann ich Artikel {i} als Geschenk verpacken lassen?"})
        verlauf.append({"role": "assistant", "content": (
            f"Ja, Artikel {i} verpacken wir gern als Geschenk. Die Geschenkverpackung kostet zwei Euro "
            "pro Artikel und wird im Warenkorb ausgewählt. Eine Grußkarte legen wir kostenlos dazu.")})
    verlauf.append({"role": "user", "content": letzte_frage})
    return verlauf


FRAGEN = {
    "Bestellnummer?": "Welche Bestellnummer habe ich dir am Anfang genannt?",
    "Katzengedicht": GEDICHT.strip(),
}

print("Runden | letzte Frage   | wir zählen | laut Ollama | richtig    | eine Antwort")
for runden in [40, 60]:
    for name, frage in FRAGEN.items():
        verlauf = gespraech(runden, frage)
        richtig = 0
        for seed in range(1, LAEUFE + 1):
            r = frage_bot(verlauf, seed)
            antwort = r.message.content.replace("\n", " ")
            # richtig heißt: die Nummer wird genannt - oder das Gedicht wird abgelehnt
            richtig += NUMMER in antwort if name == "Bestellnummer?" else regel_befolgt(antwort)
        print(f"{runden:6d} | {name:14s} | {zaehlen(verlauf):10d} | {r.prompt_eval_count:11d} "
              f"| {richtig} von {LAEUFE}  | {antwort[:50]}")
