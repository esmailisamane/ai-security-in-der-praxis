"""Erster Test: Läuft Ollama, und antwortet das Modell?"""
import ollama

MODEL = "llama3.2:3b"

response = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": "Sag Hallo in einem kurzen Satz."}],
    options={"temperature": 0, "seed": 42},  # möglichst wiederholbare Antworten
)

print("Antwort:", response.message.content)
print("Tokens in der Frage:", response.prompt_eval_count)
print("Tokens in der Antwort:", response.eval_count)
