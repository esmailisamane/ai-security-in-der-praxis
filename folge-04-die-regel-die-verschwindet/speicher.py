"""Was kostet ein größeres Kontextfenster? Wir laden das Modell mit vier Größen und fragen `ollama ps`."""
import subprocess

import ollama

from shopfix import MODEL

for num_ctx in [4096, 8192, 16384, 32768]:
    ollama.chat(model=MODEL, messages=[{"role": "user", "content": "Hallo"}],
                options={"num_ctx": num_ctx, "num_predict": 1})
    ps = subprocess.run(["ollama", "ps"], capture_output=True, text=True).stdout.splitlines()
    if num_ctx == 4096:
        print(ps[0])  # Kopfzeile: NAME, ID, SIZE, PROCESSOR, CONTEXT, UNTIL
    print(ps[-1])
