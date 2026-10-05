"""Gleiches Wort, anderer Tokenizer: Llama 3 (unser Modell) gegen GPT-4o (öffentlicher Tokenizer o200k_base).

Zusätzlich nötig: pip install tiktoken  (Claude und Gemini haben keinen öffentlichen Tokenizer.)
"""
import tiktoken
from tokenizers import Tokenizer

llama = Tokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct")
gpt4o = tiktoken.encoding_for_model("gpt-4o")
print("GPT-4o nutzt:", gpt4o.name, "\n")

for wort in ["Rabattcode", "niemals", " niemals", "Rückerstattungspolitik"]:
    l_ids = llama.encode(wort, add_special_tokens=False).ids
    g_ids = gpt4o.encode(wort)
    print(f"{wort!r}")
    print(f"  Llama 3: {[llama.decode([i]) for i in l_ids]}")
    print(f"  GPT-4o:  {[gpt4o.decode([i]) for i in g_ids]}\n")
