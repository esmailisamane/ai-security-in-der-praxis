"""Gleiche Antwort = richtige Antwort? Dieselbe Wissensfrage 10-mal pro temperature, ohne Seed.
Gezählt wird, wie oft die richtige Schreibweise "Canberra" vorkommt."""
import ollama

MODEL = "llama3.2:3b"
FRAGE = "Wie heißt die Hauptstadt von Australien? Antworte mit einem Wort."
LAEUFE = 10

for temperature in [0, 0.8, 1.5]:
    richtig, antworten = 0, []
    for _ in range(LAEUFE):
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": FRAGE}],
            options={"temperature": temperature},
        )
        antwort = response.message.content.strip()
        antworten.append(antwort)
        if "canberra" in antwort.lower():
            richtig += 1
    print(f"temperature {temperature}: {richtig} von {LAEUFE} richtig")
    print("   Antworten:", " | ".join(sorted(set(antworten))))
