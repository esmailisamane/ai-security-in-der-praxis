# AI Security in der Praxis – KI-Anwendungen sicher bauen

Der Code und alle echten Messergebnisse zum YouTube-Kurs **„AI Security in der Praxis“** vom Kanal **KIwi – KI einfach erklärt**.

Ziel des Kurses: Am Ende kannst du eine Anwendung mit Sprachmodell (LLM) sicher entwerfen, bauen, testen und betreiben.
Die Kernidee: Sicherheit entsteht vor allem durch die **Architektur** deiner Anwendung – Filter und Guardrails sind
wichtige zusätzliche Schichten, aber nicht das Fundament.

- Alles läuft **lokal und kostenlos** mit [Ollama](https://ollama.com) und einem kleinen, freien Modell (`llama3.2:3b`).
- Durch den ganzen Kurs zieht sich ein Projekt: **ShopFix**, der Support-Bot für einen erfundenen Online-Shop.
- Jede Zahl im Video stammt aus einem echten Lauf; die Ausgaben liegen im Ordner `outputs/` der jeweiligen Folge.
  Sprachmodelle sind nicht vollständig deterministisch – deine Ergebnisse können abweichen.

## Folgen

| Folge | Thema | Ordner |
|---|---|---|
| 0 | Worum geht es in diesem Kurs? (Einführung, ohne Code) | [folge-00-einfuehrung](folge-00-einfuehrung) |
| 1 | Dein KI-Labor: Ollama, Modell, Python, temperature und seed | [folge-01-ki-labor](folge-01-ki-labor) |

Weitere Folgen kommen nach und nach dazu. Der Plan wird laufend aktualisiert.

## Voraussetzungen
- Grundkenntnisse in Python
- Python 3.10 oder neuer, Windows / macOS / Linux
- Eine Grafikkarte hilft, ist aber nicht nötig

## Wichtig
Angriffe werden im Kurs nur so weit gezeigt, wie man sie zum Verstehen der Abwehr braucht.
**Teste Angriffe nur an deinen eigenen Systemen oder mit ausdrücklicher Erlaubnis.**

Siehe auch: [Glossar](GLOSSAR.md) · Lizenz für den Code: [MIT](LICENSE)
