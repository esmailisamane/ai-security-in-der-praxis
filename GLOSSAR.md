# Glossar

Fachbegriffe aus dem Kurs, kurz erklärt. Wird mit jeder Folge erweitert.

| Begriff | Bedeutung |
|---|---|
| **Sprachmodell (LLM)** | Programm, das Text liest und passenden Text zurückschreibt – die Technik hinter Chatbots wie ChatGPT. |
| **Prompt** | Der Text, den das Sprachmodell als Eingabe bekommt. |
| **System-Prompt** | Anweisungen der Entwickler an das Modell, z. B. „Du bist der Support für unseren Shop“. |
| **Prompt Injection** | Text (vom Nutzer, aus einer E-Mail, einem Dokument …), der das Modell dazu bringt, etwas anderes zu tun als geplant. Platz 1 der OWASP-Risiken für LLM-Anwendungen. |
| **Guardrails (Leitplanken)** | Prüfungen vor und nach dem Modell, z. B. ein Filter für gefährliche Eingaben. Eine zusätzliche Schicht, kein Fundament. |
| **OWASP** | Gemeinnützige Organisation für Software-Sicherheit; veröffentlicht u. a. die „Top 10“ der Risiken für LLM-Anwendungen. |
| **Ollama** | Kostenloses Programm, das Sprachmodelle auf dem eigenen Rechner ausführt. |
| **Parameter** | Die gelernten Zahlen im Inneren eines Modells; `llama3.2:3b` hat rund drei Milliarden davon. |
| **Token** | Ein kleines Textstück (ganzes Wort, Silbe, Buchstabe oder Satzzeichen) mit einer festen Nummer. Das Modell sieht nur diese Nummern, keine Buchstaben (Folge 2). |
| **temperature** | Steuert, wie viel Zufall bei der Wahl des nächsten Textstücks im Spiel ist (0 = praktisch immer das wahrscheinlichste). |
| **seed** | Startwert für den Zufall; gleicher Seed → (auf gleicher Hardware/Version) gleiche Antwort. |
| **Virtuelle Umgebung (venv)** | Abgetrennter Bereich für die Python-Pakete eines Projekts. |
| **Tokenizer** | Das Programm, das Text in Tokens zerlegt. Jede Modellfamilie hat ihren eigenen; gleicher Text ergibt bei anderen Modellen andere Stücke. |
| **Vokabular** | Alle Tokens, die ein Tokenizer kennt. Bei Llama 3.2: 128.256 Einträge. |
| **Byte Pair Encoding (BPE)** | Verfahren, mit dem viele Tokenizer ihre Stücke lernen: Häufige Textstücke bekommen eine eigene Nummer, seltene Wörter werden aus kleineren Stücken zusammengesetzt. |
| **Start-Token** | Spezielles Token (`<\|begin_of_text\|>`), das Ollama bei Llama vor jeden Text setzt. Deshalb zählt Ollama ein Token mehr. |
| **Embedding** | Die lange Liste von Zahlen, in die das Modell jede Token-Nummer übersetzt (bei llama3.2:3b: 3072 Zahlen). |
| **Wahrscheinlichkeit / logprobs** | Für jedes mögliche nächste Token berechnet das Modell eine Wahrscheinlichkeit. `logprobs` liefert sie als Logarithmus; `math.exp` macht wieder Prozent daraus. |
| **Autoregressiv** | Das Modell schreibt Token für Token: Jedes neue Token wird angehängt, dann wird das nächste berechnet. |
| **Halluzination** | Das Modell schreibt etwas Erfundenes, das plausibel klingt – z. B. eine Rückgaberegel, die es gar nicht gibt. |
