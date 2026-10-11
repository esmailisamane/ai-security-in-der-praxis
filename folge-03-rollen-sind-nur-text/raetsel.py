"""Das 36-Token-Rätsel: Was Ollama aus EINER Nachricht mit sechs Wörtern macht."""
import ollama
from tokenizers import Tokenizer

MODEL = "llama3.2:3b"
tok = Tokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct")

FRAGE = "Sag Hallo in einem kurzen Satz."

r = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": FRAGE}],
    options={"temperature": 0, "seed": 42, "num_predict": 1},
)
print("Ollama zählt:", r.prompt_eval_count, "Tokens\n")

# Das baut das Chat-Template des Modells aus unserer einen Nachricht:
TEILE = [
    ("Start-Token", "<|begin_of_text|>"),
    ("Kopf: system", "<|start_header_id|>system<|end_header_id|>\n\n"),
    ("Datumszeile", "Cutting Knowledge Date: December 2023\n\n"),
    ("Ende der Nachricht", "<|eot_id|>"),
    ("Kopf: user", "<|start_header_id|>user<|end_header_id|>\n\n"),
    ("UNSERE FRAGE", FRAGE),
    ("Ende der Nachricht", "<|eot_id|>"),
    ("Kopf: assistant", "<|start_header_id|>assistant<|end_header_id|>\n\n"),
]

summe = 0
for name, text in TEILE:
    ids = tok.encode(text, add_special_tokens=False).ids
    stuecke = [tok.decode([i], skip_special_tokens=False).replace("\n", "\\n") for i in ids]
    summe += len(ids)
    print(f"{name:19s} {len(ids):2d}  {' | '.join(stuecke)}")

frage = len(tok.encode(FRAGE, add_special_tokens=False).ids)
print(f"\nSumme: {summe} Tokens = {frage} (unsere Frage) + {summe - frage} (Rahmen vom Template)")
