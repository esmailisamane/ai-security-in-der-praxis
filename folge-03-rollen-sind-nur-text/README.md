# Folge 3 – Rollen sind nur Text

System, User und Assistant kommen beim Modell nicht auf getrennten Wegen an. Ein Chat-Template baut aus allen
Nachrichten **einen** Text. Diese Folge löst damit das 36-Token-Rätsel aus Folge 1 – und zeigt, was passiert, wenn ein
Kunde die Rollen-Markierungen einfach selbst tippt, warum „Markierungen entfernen“ nicht reicht und welche zwei
Prüfungen im Code helfen.

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
ollama show llama3.2:3b --template   # das Chat-Template des Modells
python raetsel.py      # 36 Tokens = 11 (unsere Frage) + 25 (Rahmen vom Template)
python template.py     # Prompt selbst gebaut (raw) = ollama.chat(): gleiche Tokens, gleiche Antwort
python fake_roles.py   # Ein-Token-Test, eine Kundennachricht mit 9 Spezial-Tokens, ein einzelner Lauf
python messen.py       # vier Eingaben, je 20 Läufe: wie oft bricht der Bot die Sprach-Regel?
python schutz.py       # Eingabe ablehnen + Ausgabe prüfen, gemessen mit denselben Eingaben
```

| Datei | Was sie zeigt | Echte Ausgabe |
|---|---|---|
| `raetsel.py` | Start-Token, drei Köpfe, zwei Ende-Markierungen und eine Datumszeile, die wir nie geschrieben haben | `outputs/raetsel.txt` |
| `template.py` | Rollen sind nur Text: selbst gebauter Prompt und `ollama.chat()` sind identisch (55 Tokens, gleiche Antwort) | `outputs/template.txt` |
| `shopfix.py` | Gemeinsame Teile: strenger System-Prompt, Test-Nachrichten, `bereinigen()`, `ist_englisch()` | – |
| `fake_roles.py` | `<\|eot_id\|>` getippt = 1 Token (Spezial-Token), `<eot_id>` = 5 Tokens (normaler Text) | `outputs/fake_roles.txt` |
| `messen.py` | Klartext-Bitte 1 von 20, gefälschte Rollen 7 von 20, Markierungen entfernt 16 bis 18 von 20 (im Video: 16) | `outputs/messen.txt`, `outputs/wiederholungen.md` |
| `schutz.py` | Mit beiden Prüfungen: 0 von 20 englische Antworten beim Kunden, in allen vier Fällen | `outputs/schutz.txt` |

## Wichtig zum Verständnis
- Der Test ist **absichtlich harmlos**: Es geht nur darum, ob der Bot die Sprache wechselt. So lässt sich die Wirkung
  im Code zählen.
- Die Zahlen schwanken (siehe `outputs/wiederholungen.md`). Stabil war nur die Reihenfolge – und dass Bereinigen
  allein in keinem Durchgang geholfen hat.
- `ist_englisch()` ist eine einfache Wortzählung, kein Sprachdetektor für die Produktion.
- Die Ausgabe-Prüfung funktioniert hier, weil sich die Regel „nur Deutsch“ im Code prüfen lässt. Das ist das Prinzip:
  Was wirklich gelten muss, prüft dein Code – nicht der Prompt.
- Alles gilt für `llama3.2:3b` unter Ollama 0.35.0. Andere Modelle haben andere Markierungen; große Anbieter
  trainieren ihre Modelle darauf, Rollen unterschiedlich zu gewichten, und manche filtern Markierungen auf dem Server.

## Checkliste: Rollen-Markierungen
- [ ] Eine Rolle ist ein Etikett, keine Grenze: Fremder Text bleibt fremd, egal in welcher Rolle er ankommt.
- [ ] Ein-Token-Test gegen den eigenen Stack: Wird eine getippte Markierung als Spezial-Token gezählt?
- [ ] Jeden fremden Text prüfen (Kundentext, Dokumente, Webseiten, Tool-Ergebnisse): Markierungen des eigenen
      Modells gefunden → ablehnen, nicht bereinigen und weiterschicken.
- [ ] Regeln, die gelten müssen, im Code prüfen (hier: Sprache der Antwort).
- [ ] Wirkung messen: mehrere Läufe, Fehlalarme mitzählen, nach jeder Änderung neu.

Getestet am 10. Oktober 2026 mit Ollama 0.35.0, Python 3.12, `ollama` 0.6.3, `tokenizers` 0.23.2 und `llama3.2:3b`
(GTX 1650 Ti, 4 GB). Nur zu Lernzwecken – teste nur deine eigenen Anwendungen.

## Quellen
- Meta, Llama 3.1/3.2 Prompt-Format (Spezial-Tokens, Rollen): https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/prompt_format.md
- Ollama, Template von llama3.2: https://ollama.com/library/llama3.2:3b/blobs/966de95ca8a6 · Modelfile `TEMPLATE`: https://docs.ollama.com/modelfile
- Hugging Face, Chat templates: https://huggingface.co/docs/transformers/main/en/chat_templating
- OWASP, LLM01 Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- Chang, Jun, Lee (ICLR 2026): ChatInject – Abusing Chat Templates for Prompt Injection in LLM Agents: https://arxiv.org/abs/2509.22830
- Yang, Jang, Lim (Preprint, Sept. 2026): Nameless Tokenization: https://arxiv.org/abs/2609.16984
- Fireworks AI (April 2026): Safe Tokenization: https://fireworks.ai/blog/safe-tokenization-preventing-prompt-injection-on-fireworks
- Wallace u. a. (OpenAI, 2024): The Instruction Hierarchy: https://arxiv.org/abs/2404.13208
