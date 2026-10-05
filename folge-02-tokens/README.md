# Folge 2 – Tokens & das nächste Token

Was ein Sprachmodell wirklich liest (Tokens = Textstücke mit Nummern), warum ein Wortfilter dabei etwas ganz anderes
sieht als das Modell – und wie das Modell seine Antwort Token für Token auswählt, auch dann, wenn es die Antwort gar
nicht kennen kann.

## Vorbereitung
Das Labor aus [Folge 1](../folge-01-ki-labor): Ollama läuft, `llama3.2:3b` ist geladen.
```bash
python -m venv .venv          # Python 3.10 oder neuer (tokenizers braucht mindestens 3.10)
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
```
Beim ersten Start lädt `tokenizers` den Llama-3.2-Tokenizer von Hugging Face (frei zugängliche Kopie
`unsloth/Llama-3.2-3B-Instruct`; das offizielle Meta-Repository verlangt eine Anmeldung). Die Warnung
„unauthenticated requests to the HF Hub“ ist harmlos.

## Die Skripte
```bash
python tokens.py            # Text -> Tokens und Nummern, Gegencheck mit Ollamas Zählung
python wortfilter.py        # ein Wortfilter auf den Rabattcode - und was sich für das Modell ändert
python next_token.py        # die Wahrscheinlichkeiten der ersten sechs Tokens (logprobs)
python next_token_regel.py  # dieselbe Frage ohne und mit der echten Regel des Shops
```
Zusätzlich (nicht im Video ausgeführt, aber erwähnt):
```bash
python gegenprobe.py        # 12 schwierige Texte: zählt die Kopie wie Ollama? (12 von 12)
pip install tiktoken
python vergleich_gpt4o.py   # dasselbe Wort mit dem Tokenizer von GPT-4o
```

| Datei | Was sie zeigt | Echte Ausgabe |
|---|---|---|
| `tokens.py` | „niemals“ = 3 Tokens, NIEMALS = 3 ganz andere Nummern, Ziffern in Dreiergruppen, Ollama zählt +1 Start-Token | `outputs/tokens.txt` |
| `wortfilter.py` | `VIP-7731` wird blockiert, `VIP 7731` nicht – für das Modell ändert sich genau eine von zehn Nummern | `outputs/wortfilter.txt` |
| `next_token.py` | „Ja“ mit 43–45 %, obwohl der Bot die Rückgaberegeln gar nicht kennt | `outputs/next_token.txt`, `outputs/wiederholungen.md` |
| `next_token_regel.py` | mit der Regel im System-Prompt: „Le“ (= „Leider“) mit 94 % | `outputs/next_token_regel.txt` |
| `gegenprobe.py` | Umlaute, Emojis, Code, URLs …: 12 von 12 Zählungen stimmen mit Ollama überein | `outputs/gegenprobe.txt` |
| `vergleich_gpt4o.py` | „ niemals“ ist bei GPT-4o ein einziges Token, bei Llama 3 drei | `outputs/vergleich_gpt4o.txt` |

`math.exp`: Ollama liefert `logprob` als natürlichen Logarithmus (geprüft: die Wahrscheinlichkeiten der 20 besten
Kandidaten ergeben zusammen 94–100 %). `math.exp` macht daraus wieder eine normale Wahrscheinlichkeit.

## Wichtig zum Verständnis
- Der Wortfilter ist **absichtlich naiv**. Er zeigt das Problem, er ist kein Vorschlag für einen Schutz.
  Besser: Ein Geheimnis, das der Bot gar nicht kennt, kann er auch nicht verraten.
- Eine Regel im System-Prompt gibt dem Modell den Fakt – sie ist aber **kein Schutz**: Sie ist nur Text, genau wie die
  Nachricht des Kunden. Darum geht es in Folge 3.
- Alle Nummern gelten für den Llama-3-Tokenizer. Andere Modelle zerlegen Text anders.

Getestet am 4. Oktober 2026 mit Ollama 0.35.0, Python 3.12, `ollama` 0.6.3, `tokenizers` 0.23.2, `tiktoken` 0.14.0
und `llama3.2:3b` (GTX 1650 Ti, 4 GB). Prozentzahlen schwanken leicht von Lauf zu Lauf (gemessen: 39–45 % für „Ja“).

## Quellen
- Llama-3-Tokenizer (tiktoken/BPE, 256 Spezial-Tokens, Ziffern in Gruppen bis 3): https://github.com/meta-llama/llama3/blob/main/llama/tokenizer.py
- Meta: „Introducing Meta Llama 3“ (Vokabular 128K): https://ai.meta.com/blog/meta-llama-3/
- Sennrich, Haddow, Birch (2016): Neural Machine Translation of Rare Words with Subword Units: https://arxiv.org/abs/1508.07909
- Petrov u. a. (NeurIPS 2023): Language Model Tokenizers Introduce Unfairness Between Languages: https://arxiv.org/abs/2305.15425
- Jurafsky & Martin, Speech and Language Processing (3. Aufl., Entwurf), Kap. 7: https://web.stanford.edu/~jurafsky/slp3/
- Kalai, Nachum, Vempala, Zhang (2025): Why Language Models Hallucinate: https://arxiv.org/abs/2509.04664
- Ollama API (raw, prompt_eval_count, logprobs): https://docs.ollama.com/api/generate · https://docs.ollama.com/api/chat
- Anthropic Pricing (Preise pro Million Tokens, Faustregel, neuer Tokenizer): https://platform.claude.com/docs/en/about-claude/pricing
