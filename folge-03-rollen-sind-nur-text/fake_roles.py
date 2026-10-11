"""Gefälschte Rollen: Was passiert, wenn ein Kunde die Markierungen einfach selbst tippt?"""
import ollama
from tokenizers import Tokenizer

from shopfix import FRAGE, GEFAELSCHT, MODEL, SYSTEM

tok = Tokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct")

# 1) Der Ein-Token-Test: Zählt Ollama eine getippte Markierung als Text oder als Spezial-Token?
print("--- Ein-Token-Test ---")
for text in ["<|eot_id|>", "<eot_id>"]:
    r = ollama.generate(model=MODEL, prompt=text, raw=True, options={"num_predict": 1})
    print(f"{text:12s} -> {r.prompt_eval_count - 1} Token(s)")  # minus 1 Start-Token

# 2) Die Kundennachricht - und was der Tokenizer daraus macht
print("\n--- Die eine Kundennachricht ---")
print(GEFAELSCHT)
ids = tok.encode(GEFAELSCHT, add_special_tokens=False).ids
spezial = [tok.decode([i], skip_special_tokens=False) for i in ids if i >= 128000]
print(f"\n{len(ids)} Tokens, davon {len(spezial)} Spezial-Tokens:")
print(" ".join(spezial))

# 3) Dieselbe Frage: einmal normal, einmal mit gefälschten Rollen
print("\n--- Antworten (temperature 0) ---")
for name, text in [("normal", FRAGE), ("gefälscht", GEFAELSCHT)]:
    r = ollama.chat(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}],
        options={"temperature": 0, "seed": 42, "num_predict": 40},
    )
    antwort = r.message.content.replace("\n", " ")
    print(f"{name:10s} | {r.prompt_eval_count} Tokens | {antwort}")
