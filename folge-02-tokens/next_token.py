"""Das Modell wählt Token für Token: die Kandidaten mit ihren Wahrscheinlichkeiten."""
import math

import ollama

MODEL = "llama3.2:3b"
SYSTEM = "Du bist der Support-Bot von ShopFix. Antworte kurz."

r = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "Kann ich meine Bestellung zurückschicken?"},
    ],
    options={"temperature": 0, "seed": 42, "num_predict": 6},
    logprobs=True,
    top_logprobs=3,
)

for step in r.logprobs:
    top = step.top_logprobs
    candidates = ", ".join(f"{c.token!r} {math.exp(c.logprob):.0%}" for c in top)
    print(f"gewählt: {step.token!r:14} | Kandidaten: {candidates}")
