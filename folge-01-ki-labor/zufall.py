"""Wie zufällig antwortet das Modell? Dieselbe Frage, drei Einstellungen, je drei Läufe."""
import ollama

MODEL = "llama3.2:3b"
FRAGE = "Sag Hallo in einem kurzen Satz."

EINSTELLUNGEN = {
    "temperature 0.8, ohne seed": {"temperature": 0.8},
    "temperature 0.8, seed 42": {"temperature": 0.8, "seed": 42},
    "temperature 0, seed 42": {"temperature": 0, "seed": 42},
}

for name, options in EINSTELLUNGEN.items():
    print(f"--- {name}")
    for lauf in range(1, 4):
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": FRAGE}],
            options=options,
        )
        print(f"Lauf {lauf}:", response.message.content)
