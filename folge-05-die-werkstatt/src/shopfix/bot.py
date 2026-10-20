"""Der einzige Weg zu ShopFix: Oberfläche, Tests und Scorecard rufen alle antworte() auf."""
from dataclasses import dataclass

import ollama

from shopfix.config import laden
from shopfix.prompt import nachrichten
from shopfix.schutz import MARKER, Gekuerzt, ist_englisch, zaehlen

MARKER_TEXT = "Deine Nachricht enthält Zeichenfolgen, die wir nicht verarbeiten. Bitte formuliere sie neu."
ZU_LANG = "Dein Text ist zu lang für mich. Bitte schick nur den Abschnitt, um den es geht."
ERSATZ = "Das kann ich gerade nicht beantworten. Unser Support-Team meldet sich bei dir."


@dataclass
class Antwort:
    status: str  # "ok", "abgelehnt" (nie gesendet) oder "ersetzt" (Ausgabe-Prüfung)
    text: str


def antworte(text, seed=None):
    e = laden()
    if MARKER.search(text):                      # Folge 3: gefälschte Rollen gar nicht erst senden
        return Antwort("abgelehnt", MARKER_TEXT)
    anfrage = nachrichten(text)
    gezaehlt = zaehlen(anfrage)
    if gezaehlt > e.grenze:                      # Folge 4: zu lang heißt ablehnen, nicht still kürzen
        return Antwort("abgelehnt", ZU_LANG)
    optionen = {"temperature": e.temperature, "num_ctx": e.num_ctx, "num_predict": e.antwort_budget}
    if seed is not None:
        optionen["seed"] = seed                  # gleicher Seed = wiederholbarer Lauf
    r = ollama.chat(model=e.modell, messages=anfrage, options=optionen)
    if r.prompt_eval_count != gezaehlt:          # Folge 4: ist wirklich alles angekommen?
        raise Gekuerzt(f"geschickt: {gezaehlt} Tokens, angekommen: {r.prompt_eval_count}")
    if ist_englisch(r.message.content):          # Folge 3: die Regel "Deutsch" prüft der Code
        return Antwort("ersetzt", ERSATZ)
    return Antwort("ok", r.message.content)
