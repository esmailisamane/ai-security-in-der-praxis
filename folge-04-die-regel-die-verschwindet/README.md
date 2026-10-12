# Folge 4 – Die Regel, die verschwindet

Ein Sprachmodell liest nur, was in sein **Kontextfenster** passt. Ist eine Anfrage länger, kürzt Ollama sie in der
Standardeinstellung still: kein Fehler, nur eine Warnung im Server-Log. Diese Folge zeigt, was dabei verloren geht
(der System-Prompt und die vordere Hälfte des Textes), wo es im Quellcode steht, warum auch die Antwort Platz braucht –
und einen Längen-Schutz, der vor dem Senden zählt und lieber ablehnt als still kürzt.

## Vorbereitung
Das Labor aus [Folge 1](../folge-01-ki-labor): Ollama läuft, `llama3.2:3b` ist geladen.
```bash
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
```

## Die Skripte
```bash
ollama show llama3.2:3b    # context length 131072: so viel kann das Modell
ollama ps                  # CONTEXT 4096: so viel gibt ihm der Server (nach einer ersten Anfrage)
python zu_lang.py          # immer längerer Text, je 20 Läufe: hält die Regel?
python was_bleibt.py       # die Kürzung nachgebaut: das sieht das Modell noch
python halbes_dokument.py  # auch das Dokument ist halbiert: falsche Antwort mit erfundenem Abschnitt
python verlauf.py          # langes Gespräch: die ältesten Nachrichten fallen weg
python speicher.py         # was ein größeres Fenster an Speicher kostet
python grenze.py           # die Grenze auf das Token genau – und die Antwort, die nicht mehr passt
python schalter.py         # Ollamas Schalter num_keep und truncate
python schutz.py           # Längen-Schutz: zählen, ablehnen, nachprüfen
```

| Datei | Was sie zeigt | Echte Ausgabe |
|---|---|---|
| `shopfix.py` | Gemeinsame Teile: Regel im System-Prompt, langes Dokument, `regel_befolgt()`, `zaehlen()` | – |
| `zu_lang.py` | 10 / 100 / 200 Zeilen: Regel 20 von 20. 250 / 400 Zeilen: nur 2050 Tokens kommen an, Regel 0 von 20 | `outputs/zu_lang.txt` |
| `was_bleibt.py` | 4593 Tokens → 2050: es bleiben 4 Tokens vom Anfang (der Kopf `system`) und das Ende; roh geschickt ergibt derselbe Rest dieselbe Antwort | `outputs/was_bleibt.txt` |
| `halbes_dokument.py` | Ausnahme in Abschnitt 7: bei 100 Zeilen richtig, bei 250 Zeilen „Ja … (Abschnitt 140)“ | `outputs/halbes_dokument.txt` |
| `verlauf.py` | 40 Runden passen; bei 60 Runden ist die Bestellnummer vom Anfang weg – und am Rand des Fensters auch die Regel | `outputs/verlauf.txt` |
| `speicher.py` | `ollama ps` für num_ctx 4096 bis 32768: 2,9 GB bis 6,4 GB (auf einer 4-GB-Grafikkarte) | `outputs/speicher.txt` |
| `grenze.py` | Unsere Zählung = `prompt_eval_count`. 221 Zeilen: alles gut. 222: Eingabe passt, Antwort nicht (Context Shift). 223: Eingabe gekürzt | `outputs/grenze.txt` |
| `schalter.py` | `num_keep` rettet die Regel, das Dokument wird trotzdem still halbiert; `"truncate": false` → HTTP 400 | `outputs/schalter.txt` |
| `schutz.py` | Zählen + Antwort-Budget + Nachprüfen: Regel gebrochen 0 von 20, bei jeder Länge | `outputs/schutz.txt` |

## Die Rechnung aus dem Quellcode
Ollama, `llm/llama_server.go` (Funktionen `completionPromptForRequest` und `contextShiftPromptLimit`):
```
limit = num_ctx - (num_ctx - num_keep) / 2      # 4096 - (4096 - 4) / 2 = 2050
bleibt: die ersten num_keep Tokens (Standard 4) + die letzten (limit - num_keep) Tokens
```
Im Log: `level=WARN msg="truncating input prompt" limit=2050 prompt=4593 keep=4 new=2050`

## Server-Log durchsuchen
```powershell
# Windows (PowerShell)
Select-String -Path "$env:LOCALAPPDATA\Ollama\server.log" -Pattern "truncating input prompt"
```
```bash
# macOS
grep "truncating input prompt" ~/.ollama/logs/server.log
# Linux (systemd)
journalctl -u ollama --no-pager | grep "truncating input prompt"
```

## Kontextfenster einstellen
- pro Anfrage: `options={"num_ctx": 8192}`
- für den ganzen Server: Umgebungsvariable `OLLAMA_CONTEXT_LENGTH=8192`
- in der Ollama-App: Schieberegler in den Einstellungen
- aktueller Wert: `ollama ps`, Spalte CONTEXT. Ein größeres Fenster braucht mehr Speicher.

## Wichtig zum Verständnis
- Der Test ist **absichtlich harmlos**: Es geht nur darum, ob der Bot trotz Regel ein Katzengedicht schreibt. So lässt
  sich die Wirkung im Code zählen.
- Ollama kürzt auf zwei Stufen. Zuerst fallen in einem langen Gespräch die ältesten Nachrichten weg
  (`server/prompt.go`, System-Nachrichten und die letzte Nachricht sollen bleiben; dafür gibt es keine Warnung im
  normalen Log). Passt es dann immer noch nicht, wird der fertige Text auf Token-Ebene gekürzt (die Rechnung oben).
- Das Fenster gilt für Eingabe **und** Antwort. Passt die Antwort nicht mehr hinein, verschiebt Ollama den Kontext
  mitten im Schreiben (im Log: `context shift`) – auch dabei geht der Anfang verloren.
- `"truncate": false` ist für `/api/chat` nicht in der API-Dokumentation beschrieben (nur für `/api/embed`), steht aber
  im Quellcode (`api/types.go`). Die Python-Bibliothek 0.6.3 reicht den Schalter nicht durch. Deshalb ist er hier nur
  die zweite Sicherung, nicht der Schutz selbst.
- `zaehlen()` passt zum Chat-Template von `llama3.2` (Rahmen 25 Tokens bei System- und einer Kundennachricht, siehe
  Folge 3). Ein anderes Modell hat einen anderen Rahmen – die Nachprüfung in `schutz.py` meldet das.
- Andere Systeme verhalten sich anders (manche lehnen zu lange Eingaben mit einem Fehler ab). Prüfe deinen eigenen Stack.

## Checkliste: Kontextfenster
- [ ] Fenstergröße kennen (`ollama ps`) und ausdrücklich setzen (`num_ctx`), nicht dem Standardwert überlassen.
- [ ] Vor dem Senden zählen: Inhalte aller Nachrichten + Rahmen des Chat-Templates.
- [ ] Platz für die Antwort freihalten (Antwort-Budget) und die Antwortlänge begrenzen (`num_predict`).
- [ ] Zu lang → ablehnen oder bewusst im eigenen Code kürzen, nie still dem Server überlassen.
- [ ] Nach jeder Antwort prüfen: `prompt_eval_count` == eigene Zählung.
- [ ] Server-Log regelmäßig nach `truncating input prompt` durchsuchen.

Getestet am 11. Oktober 2026 mit Ollama 0.35.0 und 0.40.3 (gleiche Ergebnisse, siehe `outputs/wiederholungen.md`), Python 3.12, `ollama` 0.6.3, `tokenizers` 0.23.3 und `llama3.2:3b`
(GTX 1650 Ti, 4 GB). Nur zu Lernzwecken – teste nur deine eigenen Anwendungen.

## Quellen
- Ollama, Context length: https://docs.ollama.com/context-length · FAQ: https://docs.ollama.com/faq · Logs: https://docs.ollama.com/troubleshooting
- Ollama, Quellcode der Kürzung: https://github.com/ollama/ollama/blob/v0.40.3/llm/llama_server.go#L282-L334 · Gesprächsverlauf: https://github.com/ollama/ollama/blob/v0.40.3/server/prompt.go
- Ollama, API `POST /api/chat`: https://docs.ollama.com/api/chat
- Anthropic, Context windows (Definition, Verhalten bei zu langer Eingabe): https://platform.claude.com/docs/en/build-with-claude/context-windows
- OpenAI, Conversation state (Definition Kontextfenster): https://developers.openai.com/api/docs/guides/conversation-state
- OWASP Top 10 for LLM Applications 2026, LLM06:2026 Unbounded Consumption (Input Size Validation): https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
