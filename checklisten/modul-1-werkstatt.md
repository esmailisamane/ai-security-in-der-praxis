# Checkliste Modul 1 – Die Werkstatt

Für dein eigenes Projekt mit einem Sprachmodell. Gezeigt in [Folge 5](../folge-05-die-werkstatt).

## Projekt & Konfiguration
- [ ] Ein Projekt mit festem Aufbau (z. B. `uv init --package`, src-Layout, Ordner `tests/`).
- [ ] Erzeugte Dateien vor dem Veröffentlichen ansehen – z. B. trägt `uv init` ohne `--author-from none` Name und E-Mail ein.
- [ ] Einstellungen (Modell, Kontextfenster, Antwort-Budget, Temperature) kommen von außen, nicht aus dem Code.
- [ ] Zugangsdaten nie im Code und nie im Git-Repository; `.env` steht in `.gitignore`.
- [ ] Falsche Einstellungen scheitern laut (Fehler beim Start), nicht still.
- [ ] Genau eine Tür: Oberfläche, Tests und Messungen rufen dieselbe Funktion auf.

## Tests
- [ ] Schnelle Tests für deinen eigenen Code (Schutzschichten, Grenzen, Web-Endpunkte) – ohne Modell, bei jeder Änderung.
- [ ] Tests mit Modell eigens markieren (z. B. `@pytest.mark.modell`) und als **Quote** prüfen, nicht als einzelnen Lauf.
- [ ] Vorher festlegen, was als Erfolg zählt (z. B. „genau der feste Satz“).
- [ ] Die Schwelle (z. B. untere Grenze ≥ 90 %) danach wählen, wie teuer ein Fehler ist.

## Messen
- [ ] Nie einen einzelnen Lauf melden: immer „x von n“ mit 95-%-Bereich (z. B. Wilson-Intervall).
- [ ] Mehrere Seeds UND mehrere Formulierungen testen.
- [ ] Temperature nicht senken, nur damit Tests ruhiger werden – das versteckt die anderen Antworten.
- [ ] Faustregel: Für einen halb so breiten Bereich ungefähr viermal so viele Läufe.

## Scorecard
- [ ] Eine feste Sammlung harmloser Angriffe, die du nach jeder Änderung neu misst.
- [ ] Drei Zahlen: Angriffe, die durchkommen · normale Nutzer zu Unrecht abgewiesen · normale Nutzer richtig geholfen.
- [ ] Versionen (Modell mit Kennung, Server, Bibliotheken) gehören zu jeder Messung.
- [ ] Alle Antworten speichern und stichprobenartig von Hand prüfen – automatische Prüfregeln irren sich.

## Betrieb
- [ ] Beim Entwickeln lauscht die App nur auf `127.0.0.1` (`fastapi dev`); `0.0.0.0` (`fastapi run`) nur bewusst, z. B. im Container.
