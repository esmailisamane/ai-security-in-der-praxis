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
| **Token** | Ein kleines Textstück (oft ein Wort oder Wortteil), mit dem ein Modell rechnet. Ausführlich in Folge 2. |
| **temperature** | Steuert, wie viel Zufall bei der Wahl des nächsten Textstücks im Spiel ist (0 = praktisch immer das wahrscheinlichste). |
| **seed** | Startwert für den Zufall; gleicher Seed → (auf gleicher Hardware/Version) gleiche Antwort. |
| **Virtuelle Umgebung (venv)** | Abgetrennter Bereich für die Python-Pakete eines Projekts. |
