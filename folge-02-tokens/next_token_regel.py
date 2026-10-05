"""Dieselbe Frage - einmal ohne und einmal mit der echten Regel des Shops."""
import math

import ollama

MODEL = "llama3.2:3b"
FRAGE = "Kann ich meine Bestellung zurückschicken?"
PROMPTS = {
    "ohne Regel": "Du bist der Support-Bot von ShopFix. Antworte kurz.",
    "mit Regel": "Du bist der Support-Bot von ShopFix. Antworte kurz. "
                 "Regel: ShopFix nimmt keine Rücksendungen an.",
}

for name, system in PROMPTS.items():
    r = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": FRAGE},
        ],
        options={"temperature": 0, "seed": 42, "num_predict": 40},
        logprobs=True,
        top_logprobs=3,
    )
    first = r.logprobs[0].top_logprobs
    candidates = ", ".join(f"{c.token!r} {math.exp(c.logprob):.0%}" for c in first)
    print(f"{name}:")
    print(f"  erstes Token: {candidates}")
    print(f"  Antwort:      {r.message.content}\n")
