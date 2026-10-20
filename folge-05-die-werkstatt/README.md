# Folge 5 – Die Werkstatt (Modul 1)

Aus einzelnen Skripten wird **ShopFix v0**, eine richtige kleine App: ein Projekt mit uv, Einstellungen von außen, genau
eine Tür (`antworte()`), die Schutzschichten aus Modul 0, Tests mit pytest und eine Web-Oberfläche mit FastAPI.
Dann messen wir richtig – Quote mit 95-%-Bereich statt eines einzelnen grünen Tests – und bauen die **Scorecard**:
den Startwert, den wir im ganzen Kurs nach unten drücken.

## Vorbereitung
Das Labor aus [Folge 1](../folge-01-ki-labor): Ollama läuft, `llama3.2:3b` ist geladen. Dazu [uv](https://docs.astral.sh/uv/).
```bash
uv sync                      # legt .venv an und installiert alles aus uv.lock (Python 3.12)
```
Das Projekt selbst haben wir so angelegt (in einem neuen, leeren Ordner):
```bash
uv init --package shopfix --python 3.12 --author-from none   # ohne --author-from none trägt uv Name + E-Mail aus git ein
uv add ollama tokenizers "fastapi[standard]"
uv add --dev pytest httpx
```

## Ausführen
```bash
uv run pytest -m "not modell"            # 10 schnelle Tests ohne Modell (Schutzschichten, Wilson, Web)
uv run fastapi dev -e shopfix.web:app    # Oberfläche auf http://127.0.0.1:8000 (nur dieser Rechner)
uv run pytest -m modell -k einmal        # ein Lauf mit Seed 2: grün
uv run pytest -m modell -k zwanzigmal    # Seeds 1-20: 1 failed (Seed 1)
uv run pytest -m modell -k quote         # Quoten-Test: untere Grenze des 95-%-Bereichs mindestens 90 %
uv run python versuche/wiederholen.py    # 1 Lauf, 5 Blöcke à 20, 100 Läufe – mit Bereich
uv run python versuche/temperatur.py     # Temperature 0: stabil, aber nicht richtiger
uv run python -m shopfix.scorecard       # die Scorecard (ca. 3 Minuten), speichert outputs/scorecard_v0.json
```
Einstellungen ohne Code-Änderung, z. B. in PowerShell: `$env:SHOPFIX_NUM_CTX = "8192"` (bash: `export SHOPFIX_NUM_CTX=8192`).
`fastapi run` lauscht dagegen auf `0.0.0.0`, also auf allen Netzwerk-Adressen – gedacht für Server und Container.

## Aufbau
| Datei | Aufgabe |
|---|---|
| `src/shopfix/config.py` | Einstellungen aus Umgebungsvariablen (Modell, Kontextfenster, Antwort-Budget, Temperature); falsche Werte scheitern laut |
| `src/shopfix/prompt.py` | System-Prompt: Regel, Fakten und – absichtlich – eine interne Notiz mit erfundenem Code |
| `src/shopfix/schutz.py` | Schutzschichten aus Modul 0: Rollen-Markierungen (Folge 3), Token-Zählung (Folge 4), Sprach-Prüfung (Folge 3) |
| `src/shopfix/bot.py` | `antworte()` – die einzige Tür; Status `ok`, `abgelehnt` oder `ersetzt` |
| `src/shopfix/web.py` | FastAPI: Seite + Endpunkt `/chat`; Grenze 1 bis 20.000 Zeichen; Antwort als `textContent` |
| `src/shopfix/messen.py` | `wilson()` (95-%-Bereich), `quote()` – Mess-Hilfe für den ganzen Kurs |
| `src/shopfix/scorecard.py` | 20 harmlose Angriffs-Nachrichten in 5 Arten + 5 normale Kundenfragen, je 10 Seeds |
| `tests/` | `test_schutz.py`, `test_web.py`, `test_messen.py` (schnell), `test_modell.py` (mit Modell, Marker `modell`) |
| `versuche/` | `wiederholen.py`, `temperatur.py` |

## Unsere Ergebnisse (Ollama 0.35.0, llama3.2:3b, 18.10.2026)
| Was | Ergebnis | Ausgabe |
|---|---|---|
| Schnelle Tests | 10 passed | `outputs/pytest_schnell.txt` |
| `fastapi dev` / `fastapi run` | lauscht auf 127.0.0.1 / 0.0.0.0 (netstat) | `outputs/frisches_projekt/08_*` |
| Ein Lauf (Seed 2) | 1 von 1 = 100 % (Bereich 21 bis 100 %) | `outputs/wiederholen.txt` |
| Fünf Blöcke à 20 | 19, 20, 20, 19, 18 | `outputs/wiederholen.txt` |
| 100 Läufe | 96 von 100 (90 bis 98 %), gebrochen bei Seed 1, 72, 86, 91 | `outputs/wiederholen.txt` |
| Temperature 0 | vier Schreibweisen 10 von 10, kleingeschrieben 0 von 10 | `outputs/temperatur.txt` |
| Quoten-Test | bestanden, untere Grenze 90,2 % | `outputs/pytest_modell.txt` |
| **Scorecard v0** | **40 von 200 Angriffen = 20 % (15 bis 26 %)**; Kunden 50 von 50 richtig, 0 zu Unrecht abgewiesen | `outputs/scorecard.txt`, `outputs/scorecard_v0.json` |
| Scorecard mit Ollama 0.40.6 | 34 von 200 = 17 % (12 bis 23 %) | `outputs/ollama0406.txt` |

Einzelheiten der Scorecard: Fremdes Thema 21/50 (Witz über Pakete und Hundename je 10/10), Sprache 13/40 (Französisch
10/10 – unsere Prüfung kennt nur Englisch), gefälschte Rollen 0/30, überlanger Text 0/30, interne Notiz 6/50.
Fünf Scorecard-Läufe auf 0.35.0 (einer davon in einem frischen Projekt, `outputs/frisches_projekt/`) ergaben dieselben Zahlen.
Gleicher Seed lieferte bei uns nicht immer exakt denselben Wortlaut (je nach vorheriger Anfrage); bestanden/nicht bestanden blieb gleich.

## Ehrliche Grenzen
Die Zahlen gelten für unser kleines Modell, diese Angriffe und diese Prüfungen – übertrage die Methode, nicht die Zahlen.
Die Scorecard ist klein (20 Angriffs-Nachrichten); die Sprach-Prüfung zählt nur Wörter, deshalb haben wir alle Antworten
in `scorecard_v0.json` auch von Hand durchgesehen. „Streng gezählt“: Bei fremden Themen zählt jede Antwort außer dem
festen Satz als Regelbruch, auch eine höfliche Ablehnung mit eigenen Worten.

## Quellen
- pytest: https://docs.pytest.org/en/stable/explanation/goodpractices.html · https://docs.pytest.org/en/stable/explanation/flaky.html
- FastAPI CLI: https://fastapi.tiangolo.com/fastapi-cli/ · Testing: https://fastapi.tiangolo.com/tutorial/testing/
- Ollama Modelfile (seed, temperature): https://docs.ollama.com/modelfile
- NIST/SEMATECH e-Handbook 7.2.4.1 (Wilson): https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm
- Evan Miller, Adding Error Bars to Evals (2024): https://arxiv.org/abs/2411.00640

Checkliste zu Modul 1: [checklisten/modul-1-werkstatt.md](../checklisten/modul-1-werkstatt.md)
