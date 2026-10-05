"""Gegenprobe: Zählt unsere Tokenizer-Kopie auch bei schwierigen Texten genau wie Ollama?"""
import ollama
from tokenizers import Tokenizer

MODEL = "llama3.2:3b"
tok = Tokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct")

TEXTS = [
    "Größe, Übermaß, Fußgängerüberweg",
    "Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz",
    "def f(x):\n    return x**2  # Kommentar",
    "🙂 Emoji 🚀 und ein Ä",
    "https://example.com/a?b=1&c=2",
    "   drei Leerzeichen vorne",
    "12345678901234567890",
    "ShopFix: Bestellung #A-1029 ist unterwegs.",
    "niemals",
    "Niemals",
    "NIEMALS",
    " niemals",
]

gleich = 0
for text in TEXTS:
    n = len(tok.encode(text, add_special_tokens=False).ids)
    r = ollama.generate(model=MODEL, prompt=text, raw=True, options={"num_predict": 1})
    ok = r.prompt_eval_count == n + 1  # Ollama zählt das Start-Token mit
    gleich += ok
    print(f"{text!r:48.48} unsere Zählung: {n:2}  Ollama: {r.prompt_eval_count:2}  {'OK' if ok else 'ANDERS'}")
print(f"\n{gleich} von {len(TEXTS)} stimmen überein")

for wort in ["niemals", "Niemals", "NIEMALS", " niemals"]:
    ids = tok.encode(wort, add_special_tokens=False).ids
    print(f"{wort!r:12} {[tok.decode([i]) for i in ids]}  {ids}")
print("Nummer des Start-Tokens <|begin_of_text|>:", tok.token_to_id("<|begin_of_text|>"))
