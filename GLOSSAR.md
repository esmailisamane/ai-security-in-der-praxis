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
| **Rolle** | Etikett einer Nachricht: `system` (Regeln der Entwickler), `user` (Nutzer), `assistant` (Antworten des Modells). Ein Etikett, keine Sicherheitsgrenze (Folge 3). |
| **Chat-Template** | Vorlage, die alle Nachrichten mit ihren Rollen zu EINEM Text zusammensetzt, bevor das Modell ihn bekommt. Jede Modellfamilie hat ihr eigenes Format. |
| **Spezial-Token** | Token mit Sonderbedeutung, z. B. `<\|start_header_id\|>`, `<\|end_header_id\|>`, `<\|eot_id\|>` (end of turn) bei Llama 3. Sie markieren Anfang und Ende der Nachrichten. |
| **Gefälschte Rollen** | Fremder Text, der selbst wie ein Gespräch mit Rollen aussieht (mit oder ohne Spezial-Tokens) und das Modell so zu anderem Verhalten bringt. |
| **Ein-Token-Test** | Prüfung, ob der eigene Stack eine getippte Markierung als Spezial-Token zählt (1 Token) oder als normalen Text (mehrere Tokens). |
| **Kontextfenster (Context Window)** | Alles, was ein Modell beim Antworten vor Augen hat: Regeln, Gespräch, Dokumente – und die Antwort, die es gerade schreibt. Gemessen in Tokens (Folge 4). |
| **num_ctx / Context Length** | Größe des Kontextfensters, die der Server dem Modell gibt. Bei Ollama oft 4096, obwohl das Modell mehr könnte. Anzeigen: `ollama ps`, Spalte CONTEXT. |
| **Stille Kürzung (Truncation)** | Ist eine Anfrage länger als das Fenster, kürzt Ollama sie ohne Fehlermeldung: Es bleiben die ersten `num_keep` Tokens und das Ende. Nur im Server-Log steht `truncating input prompt`. |
| **num_keep** | So viele Tokens vom Anfang bleiben bei einer Kürzung stehen (Standard: 4). |
| **Context Shift** | Läuft das Fenster beim Schreiben der Antwort voll, wirft Ollama die vordere Hälfte weg und schreibt weiter – auch dabei kann der System-Prompt verloren gehen. |
| **Antwort-Budget** | Platz im Kontextfenster, den der eigene Code für die Antwort freihält: Grenze für die Eingabe = Fenster minus Budget. |
| **Längen-Schutz** | Prüfung im eigenen Code: Tokens vor dem Senden zählen, zu lange Anfragen ablehnen statt still kürzen lassen, nach der Antwort `prompt_eval_count` nachprüfen. |
| **uv** | Werkzeug für Python-Projekte: legt die virtuelle Umgebung an, installiert Pakete und hält ihre genauen Versionen in `uv.lock` fest (Folge 5). |
| **pyproject.toml** | Der „Steckbrief“ eines Python-Projekts: Name, Python-Version, Pakete und Einstellungen für Werkzeuge wie pytest. |
| **src-Layout** | Der Code liegt in `src/<paket>/`, die Tests in `tests/`. So prüfen die Tests das installierte Paket – von der pytest-Dokumentation empfohlen. |
| **Umgebungsvariable** | Ein Wert, der außerhalb des Codes gesetzt wird (im Terminal oder auf dem Server). So läuft derselbe Code mit anderen Einstellungen. |
| **pytest** | Verbreitetes Test-Werkzeug für Python. Ein Test ist eine Funktion, deren Name mit `test` beginnt. |
| **assert** | „Stelle sicher“: Die Bedingung dahinter muss wahr sein, sonst schlägt der Test fehl und pytest zeigt den echten Wert. |
| **Marker** | Etikett für Tests, z. B. `@pytest.mark.modell`; mit `-m "not modell"` lassen sich markierte Tests auslassen. |
| **parametrize** | pytest-Werkzeug, das einen Test für mehrere Werte ausführt, z. B. für die Seeds 1 bis 20. |
| **Flaky Test (wackeliger Test)** | Ein Test, der mal besteht und mal nicht. Bei Sprachmodellen schwankt das Modell selbst – deshalb prüft man dort Quoten. |
| **FastAPI** | Python-Bibliothek für Web-Anwendungen und Schnittstellen; `fastapi dev` startet einen Entwicklungs-Server. |
| **Endpunkt** | Eine Adresse auf dem Server, an die ein Programm oder der Browser etwas schicken kann, z. B. `POST /chat`. |
| **TestClient / Attrappe** | Der TestClient spielt den Browser ohne echten Server; eine Attrappe (Mock) ersetzt beim Testen ein Teil, z. B. das Modell. |
| **127.0.0.1 / 0.0.0.0** | 127.0.0.1 = nur der eigene Rechner kommt an die App. 0.0.0.0 = die App lauscht auf allen Netzwerk-Adressen (z. B. im WLAN erreichbar). |
| **Quote** | „x von n“: wie oft etwas eingetreten ist, z. B. 96 von 100 Läufen. |
| **Konfidenzintervall (Bereich)** | Der Bereich, in dem die wahre Quote mit großer Sicherheit liegt. 95-%-Bereich: fängt die wahre Quote ungefähr bei 19 von 20 Messungen ein. |
| **Wilson-Intervall** | Rechenverfahren für den Bereich einer Quote (Wilson, 1927), empfohlen auch bei kleinen Zahlen und bei 0 oder n Treffern. |
| **Scorecard** | Feste Sammlung harmloser Angriffe und normaler Fragen, die nach jedem Modul neu gemessen wird: Angriffs-Quote, Fehlalarme, Nutzen (Folge 5). |
| **Fehlalarm** | Ein normaler Nutzer wird zu Unrecht abgewiesen. Ein Schutz, der das oft tut, ist selbst ein Fehler. |
