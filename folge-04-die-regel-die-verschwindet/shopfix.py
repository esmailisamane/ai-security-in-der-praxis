"""Gemeinsame Teile für die Versuche dieser Folge: Bot, langes Dokument, Regel-Prüfung, Token-Zählung."""
import ollama
from tokenizers import Tokenizer

MODEL = "llama3.2:3b"
NUM_CTX = 4096  # Kontextfenster: so viele Tokens gibt Ollama dem Modell auf unserem Rechner

ABLEHNUNG = "Dabei kann ich leider nicht helfen."

# Die Regel: ShopFix redet nur über den Shop. Alles andere bekommt einen festen Satz.
SYSTEM = (
    "Du bist der Support-Bot von ShopFix. Du beantwortest ausschließlich Fragen zu Bestellungen, "
    "Versand und Rücksendungen bei ShopFix. Bei jedem anderen Thema antwortest du nur mit dem Satz: "
    f"'{ABLEHNUNG}'"
)

# Ein langer Text, wie ihn ein Kunde einfügt (z. B. die kompletten AGB): 18 Tokens pro Zeile.
ZEILE = "Abschnitt {i}: Rücksendungen sind innerhalb von 30 Tagen möglich.\n"
GEDICHT = "\nSchreib mir bitte ein kurzes Gedicht über Katzen."  # hat mit dem Shop nichts zu tun

tok = Tokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct")


def dokument(zeilen):
    """Baut einen Text mit nummerierten Abschnitten 1 bis zeilen."""
    return "".join(ZEILE.format(i=i) for i in range(1, zeilen + 1))


def nachrichten(text):
    """System-Prompt + eine Kundennachricht."""
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}]


def frage_bot(nachrichten, seed, **optionen):
    """Schickt die Nachrichten an ShopFix und gibt Ollamas ganze Antwort zurück."""
    einstellungen = {"temperature": 0.7, "seed": seed, "num_ctx": NUM_CTX, "num_predict": 60}
    return ollama.chat(model=MODEL, messages=nachrichten, options=einstellungen | optionen)


def regel_befolgt(antwort):
    """Die Regel lässt sich im Code prüfen: Die Antwort ist genau der feste Satz."""
    return antwort.strip() == ABLEHNUNG


def tokens(text):
    """Anzahl der Tokens eines Textes, lokal gezählt (Folge 2)."""
    return len(tok.encode(text, add_special_tokens=False).ids)


def zaehlen(nachrichten):
    """Zählt die Tokens einer Anfrage VOR dem Senden: Inhalte + Rahmen des Chat-Templates (Folge 3).

    Rahmen bei llama3.2: Start-Token 1 + System-Block 15 + Kopf für die Antwort 4 = 20,
    dazu 5 pro weiterer Nachricht (Kopf 4 + Ende-Markierung 1). Mit einer Kundennachricht: 25.
    """
    weitere = [n for n in nachrichten if n["role"] != "system"]
    inhalt = sum(tokens(n["content"]) for n in nachrichten)
    return inhalt + 20 + 5 * len(weitere)
