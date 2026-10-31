"""Die kleine Web-Oberfläche: eine Seite und ein Endpunkt, der antworte() aufruft."""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from shopfix.bot import antworte

app = FastAPI(title="ShopFix v0")


class Frage(BaseModel):
    # Erste, grobe Grenze schon an der Tür: leere oder riesige Nachrichten prüft FastAPI selbst.
    nachricht: str = Field(min_length=1, max_length=20_000)


@app.post("/chat")
def chat(frage: Frage):
    a = antworte(frage.nachricht)
    return {"status": a.status, "antwort": a.text}


SEITE = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>ShopFix v0</title>
<style>body{font:18px system-ui;max-width:640px;margin:40px auto}textarea{width:100%;height:90px;font:inherit}
#antwort{white-space:pre-wrap;background:#f3f5f9;padding:12px;border-radius:8px;min-height:40px}</style></head>
<body><h1>ShopFix Support</h1>
<textarea id="nachricht" placeholder="Deine Frage an ShopFix"></textarea>
<p><button id="senden">Senden</button></p><div id="antwort"></div>
<script>
document.getElementById("senden").onclick = async () => {
  const r = await fetch("/chat", {method: "POST", headers: {"Content-Type": "application/json"},
    body: JSON.stringify({nachricht: document.getElementById("nachricht").value})});
  const daten = await r.json();
  // textContent zeigt die Antwort als reinen Text an – nie als HTML (wichtig in einer späteren Folge).
  document.getElementById("antwort").textContent = daten.antwort ?? "Fehler: " + r.status;
};
</script></body></html>"""


@app.get("/", response_class=HTMLResponse)
def seite():
    return SEITE
