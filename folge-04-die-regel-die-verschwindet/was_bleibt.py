"""Was sieht das Modell nach der Kürzung? Wir bauen die Kürzung nach und prüfen sie."""
import ollama

from shopfix import GEDICHT, MODEL, NUM_CTX, SYSTEM, dokument, frage_bot, nachrichten, tok

text = dokument(250) + GEDICHT

# Der eine Text, den das Chat-Template aus unseren zwei Nachrichten baut (Folge 3):
PROMPT = (
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
    "Cutting Knowledge Date: December 2023\n\n" + SYSTEM + "<|eot_id|>"
    "<|start_header_id|>user<|end_header_id|>\n\n" + text + "<|eot_id|>"
    "<|start_header_id|>assistant<|end_header_id|>\n\n"
)
ids = tok.encode(PROMPT, add_special_tokens=False).ids
print("Ganzer Prompt:", len(ids), "Tokens - das Fenster hat", NUM_CTX)

# Die Rechnung aus Ollamas Quellcode (llm/llama_server.go):
NUM_KEEP = 4                                 # so viele Tokens vom Anfang bleiben (Standard)
limit = NUM_CTX - (NUM_CTX - NUM_KEEP) // 2  # so viel bleibt insgesamt
gekuerzt = ids[:NUM_KEEP] + ids[len(ids) - (limit - NUM_KEEP):]
print("Nach der Kürzung:", len(gekuerzt), "Tokens - weggeworfen:", len(ids) - len(gekuerzt))

rest = tok.decode(gekuerzt, skip_special_tokens=False)
print("\nSo beginnt der Text, den das Modell noch sieht:")
print(rest[:200])
print("\nSteht unsere Regel noch darin?", "ausschließlich Fragen zu Bestellungen" in rest)

# Gegenprobe: derselbe gekürzte Text, roh geschickt. Kommt dieselbe Antwort heraus?
OPTIONEN = {"temperature": 0, "seed": 42, "num_ctx": NUM_CTX, "num_predict": 30}
chat = frage_bot(nachrichten(text), 42, temperature=0, num_predict=30)
roh = ollama.generate(model=MODEL, prompt=rest.removeprefix("<|begin_of_text|>"), raw=True, options=OPTIONEN)
print("\nchat():", chat.prompt_eval_count, "Tokens |", chat.message.content.replace("\n", " "))
print("roh   :", roh.prompt_eval_count, "Tokens |", roh.response.replace("\n", " "))
print("Identisch:", chat.message.content == roh.response)
