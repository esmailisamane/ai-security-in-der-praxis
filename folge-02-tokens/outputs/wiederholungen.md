# Wiederholte Läufe (2026-10-04, Ollama 0.35.0, llama3.2:3b, GTX 1650 Ti)

Gleicher Code, gleiche Optionen (temperature 0, seed 42) – trotzdem kleine Schwankungen (GPU-Nichtdeterminismus).

## next_token.py – erstes Token
- 8 Läufe: 7× "Ja" 45 % (Bitte 18 %, Um 10 %), 1× "Ja" 43 % (Bitte 20 %) → `next_token_lauf_43prozent.txt` (erster Lauf nach dem Laden)
- Zum Vergleich 2026-10-01: 7× 39 %, 1× 45 %.
- Gewähltes Token und Antwort "Ja, das ist möglich." in allen Läufen gleich.

## next_token_regel.py
- 3 Läufe mit num_predict 20 und 2 Läufe mit num_predict 40: identisch. Mit Regel: "Le" 94 % → "Leider nein, ShopFix nimmt keine Rücksendungen an."

## Läufe in der Bildschirmaufnahme (2026-10-04, gleicher Rechner)
- next_token.py: "Ja" 43 %, "Bitte" 20 %, "Um" 10 % (im Video zu sehen)
- next_token_regel.py: ohne Regel "Ja" 45 %, "Bitte" 18 %, "Um" 10 %; mit Regel "Le" 94 %, "Ne" 2 %, "Ent" 2 %
→ Gleicher Code, gleiche Frage, wenige Minuten Abstand: 43 % und 45 %. Kleine Schwankungen sind normal.
