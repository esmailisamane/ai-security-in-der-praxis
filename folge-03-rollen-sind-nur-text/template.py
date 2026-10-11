"""Rollen sind nur Text: den Prompt selbst bauen und mit ollama.chat() vergleichen."""
import ollama

MODEL = "llama3.2:3b"
OPTIONS = {"temperature": 0, "seed": 42, "num_predict": 60}

SYSTEM = "Du bist der Support-Bot von ShopFix. Antworte kurz und freundlich auf Deutsch."
USER = "Kann ich meine Bestellung noch ändern?"


def build_prompt(system, user):
    """Genau das, was das Chat-Template aus zwei Nachrichten macht."""
    return (
        "<|start_header_id|>system<|end_header_id|>\n\n"
        "Cutting Knowledge Date: December 2023\n\n"
        f"{system}<|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>\n\n"
        f"{user}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>\n\n"
    )


# Weg 1: wie üblich - eine Liste von Nachrichten mit Rollen
chat = ollama.chat(
    model=MODEL,
    messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": USER}],
    options=OPTIONS,
)

# Weg 2: alles selbst als EINEN Text bauen, ohne Template (raw)
prompt = build_prompt(SYSTEM, USER)
raw = ollama.generate(model=MODEL, prompt=prompt, raw=True, options=OPTIONS)

print("--- Der eine Text, den das Modell bekommt ---")
print(prompt)
print("--- Vergleich ---")
print("Tokens chat():", chat.prompt_eval_count, "| Tokens raw:", raw.prompt_eval_count)
print("Antwort chat():", chat.message.content)
print("Antwort raw:   ", raw.response)
print("Identisch:", chat.message.content == raw.response)
