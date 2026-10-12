# Wiederholungen (11. Oktober 2026)

Jedes Skript lief dreimal: zweimal mit Ollama 0.35.0 (`*.txt`, `*_lauf2.txt`) und einmal mit Ollama 0.40.3
(`*_ollama0403.txt`). Alle Zahlen waren in allen drei Durchgängen gleich.

| Skript | Ergebnis (alle drei Durchgänge) | Warnungen `truncating input prompt` im Log | `context shift` im Log |
|---|---|---|---|
| `zu_lang.py` | 10 / 100 / 200 Zeilen: 273 / 1893 / 3693 Tokens, Regel 20 von 20 · 250 / 400 Zeilen: 2050 Tokens, 0 von 20 | 40 (2 Längen × 20 Läufe) | 0 |
| `was_bleibt.py` | 4593 → 2050 Tokens, Identisch: True | 1 | 0 |
| `halbes_dokument.py` | 100 Zeilen: 10 von 10 richtig · 250 Zeilen: 2 von 10 | 10 | 0 |
| `verlauf.py` | 40 Runden: 5 von 5 und 5 von 5 · 60 Runden: 0 von 5 und 0 von 5 | 5 (nur die Gedicht-Frage) | 4 |
| `grenze.py` | 220 / 221: 10 von 10 · 222: 0 von 10 (Antwort 50 Tokens) · 223: 2050 Tokens, 0 von 10 | 10 (223 Zeilen) | 10 (222 Zeilen) |
| `schalter.py` | num_keep 4: 0 von 10 · num_keep 71: 2084 Tokens, 10 von 10 · truncate=false: HTTP 400 | 20 | 0 |
| `schutz.py` | abgelehnt ab 222 Zeilen, Regel gebrochen 0 von 20 in jeder Zeile | 0 | 0 |
| `speicher.py` | 2,9 / 3,4 / 4,4 / 6,4 GB bei num_ctx 4096 / 8192 / 16384 / 32768 | 0 | 0 |

Zusatzprüfung zur Grenze des Schutzes (Ollama 0.40.3): Eingabe mit genau 3796 Tokens + Antwort mit 300 Tokens = 4096,
kein `context shift`. Mit 3797 Tokens Eingabe: ein `context shift`. Die Grenze „Fenster minus Antwort-Budget“ passt also
auf das Token genau.

Zum Gespräch mit 60 Runden: Mit einer Debug-Option von Ollama haben wir den fertigen Text angesehen. Die System-Nachricht
steht noch darin, die Bestellnummer nicht mehr; die erste erhaltene Frage ist die zu Artikel 9. Bei der Gedicht-Frage
kam der Text danach auf 4097 Tokens (ein Token über der Grenze der zweiten Stufe) und wurde auf 2050 gekürzt – deshalb
ging dort auch die Regel verloren.

Anders als in Folge 3 schwankten die Ergebnisse hier nicht. Der Grund: Ob die Regel im Text steht oder nicht, hängt
nicht vom Zufall ab, sondern nur von der Länge.
