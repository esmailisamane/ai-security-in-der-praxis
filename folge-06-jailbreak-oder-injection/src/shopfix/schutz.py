"""Die Schutzschichten aus Modul 0: Markierungen (Folge 3), Länge (Folge 4), Sprache der Antwort (Folge 3)."""
import os
import re
from functools import cache

# Der Tokenizer ist öffentlich, ein Hugging-Face-Token braucht man nicht – also keine Warnung deswegen.
os.environ.setdefault("HF_HUB_VERBOSITY", "error")

from tokenizers import Tokenizer  # noqa: E402

MARKER = re.compile(r"<\|[^<>|]*\|>")  # Schreibweise der Spezial-Tokens: <|...|>


class Gekuerzt(Exception):
    """Ollama hat weniger Tokens verarbeitet, als wir geschickt haben."""


@cache
def tokenizer():
    """Der Tokenizer von Llama 3.2 (Folge 2) – wird beim ersten Aufruf einmal geladen."""
    return Tokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct")


def tokens(text):
    return len(tokenizer().encode(text, add_special_tokens=False).ids)


def zaehlen(nachrichten):
    """Tokens einer Anfrage VOR dem Senden: Inhalte + Rahmen des Chat-Templates (Folge 3 und 4)."""
    weitere = [n for n in nachrichten if n["role"] != "system"]
    return sum(tokens(n["content"]) for n in nachrichten) + 20 + 5 * len(weitere)


DEUTSCH = re.compile(
    r"\b(der|die|das|und|ist|wir|nicht|für|von|ich|sie|eine?|zu|mit|auf|dauert|versand|"
    r"werktage?n?|bestellung|hallo)\b", re.I)
ENGLISCH = re.compile(
    r"\b(the|and|is|we|our|your|you|for|of|to|with|shipping|usually|days|order|delivery|"
    r"hello|typically)\b", re.I)


def ist_englisch(text):
    """Einfache Prüfung aus Folge 3: mehr englische als deutsche Alltagswörter?"""
    return len(ENGLISCH.findall(text)) > len(DEUTSCH.findall(text))
