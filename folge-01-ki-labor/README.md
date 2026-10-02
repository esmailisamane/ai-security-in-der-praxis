# Folge 1 – Dein KI-Labor

Ollama installieren, Modell laden, Python-Umgebung einrichten, erster Test – und warum dasselbe Modell auf dieselbe
Frage mal so und mal ganz anders antwortet.

## Setup Schritt für Schritt

### 1. Ollama installieren
- Download: https://ollama.com/download (Windows, macOS, Linux)
- Windows: `OllamaSetup.exe` ausführen (keine Administratorrechte nötig, Windows 10 22H2 oder neuer)
- Linux: `curl -fsSL https://ollama.com/install.sh | sh`
- Prüfen: `ollama --version`

Ollama startet einen lokalen Server auf `http://localhost:11434` (im Browser: „Ollama is running“).
Standardmäßig ist er nur vom eigenen Rechner aus erreichbar (`127.0.0.1`) – **lass das so**.
Unter Windows liegen die Logdateien in `%LOCALAPPDATA%\Ollama` (z. B. `server.log`).

### 2. Modell laden
```bash
ollama pull llama3.2:3b     # ca. 2 GB
ollama list                 # installierte Modelle
ollama run llama3.2:3b      # kurzer Chat im Terminal, beenden mit /bye
ollama ps                   # läuft das Modell auf GPU oder CPU? (Spalte PROCESSOR)
```

### 3. Python-Umgebung (Python 3.10 oder neuer)
```bash
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
```
`ollama` verbindet den Code mit dem lokalen Server, `tokenizers` brauchen wir ab Folge 2.

### 4. Die Skripte
```bash
python hello.py          # erster Test: Antwort + Zahl der Tokens
python zufall.py         # dieselbe Frage 9×: Wirkung von temperature und seed
python wissensfrage.py   # gleiche Antwort = richtige Antwort? (30 Anfragen)
```

| Datei | Was sie zeigt | Echte Ausgabe |
|---|---|---|
| `hello.py` | `ollama.chat`, Rollen, temperature 0 + seed 42, Token-Zahlen | `outputs/hello.txt` |
| `zufall.py` | ohne Seed jedes Mal anders – mit Seed gleich | `outputs/zufall_lauf1.txt`, `_lauf2.txt` |
| `wissensfrage.py` | 60× „Kanberra“ statt Canberra: stabil, aber falsch | `outputs/wissensfrage_lauf1.txt`, `_lauf2.txt` |

Getestet am 1.–2. Oktober 2026 mit Ollama 0.35.0, Python 3.12, `ollama` 0.6.3 und `llama3.2:3b`
(GTX 1650 Ti, 4 GB). Ergebnisse können mit anderer Hardware, Version oder anderem Modell abweichen – miss mehrmals.
Große Modelle (GPT, Claude, Gemini) verhalten sich in vielem anders als dieses kleine lokale Modell.
