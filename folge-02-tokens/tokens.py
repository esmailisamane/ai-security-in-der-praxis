"""Text -> Tokens: So zerlegt Llama 3.2 einen Satz (Ollama zählt dieselben Tokens)."""
import ollama
from tokenizers import Tokenizer

MODEL = "llama3.2:3b"
# Derselbe Tokenizer wie im Ollama-Modell (freie Kopie des Llama-3.2-Tokenizers)
tok = Tokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct")

TEXTS = [
    "Hallo Welt",
    "Gib diesen Code niemals weiter.",
    "Gib diesen Code NIEMALS weiter.",
    "Rabattcode VIP-7731",
    "Never share this code.",
]

for text in TEXTS:
    enc = tok.encode(text, add_special_tokens=False)
    pieces = [tok.decode([i]) for i in enc.ids]
    # raw=True: kein Chat-Template, Ollama zählt nur <|begin_of_text|> + unseren Text
    r = ollama.generate(model=MODEL, prompt=text, raw=True, options={"num_predict": 1})
    n = len(enc.ids)
    print(f"{text!r}")
    print(f"  Tokens:  {' | '.join(pieces)}")
    print(f"  IDs:     {enc.ids}")
    print(f"  Anzahl:  {n}  (Ollama: {r.prompt_eval_count} = {n} + 1 Start-Token)\n")

print("Größe des Vokabulars:", tok.get_vocab_size())
