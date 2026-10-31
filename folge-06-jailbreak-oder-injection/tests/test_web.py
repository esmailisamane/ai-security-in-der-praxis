"""Die Oberfläche testen, ohne das Modell zu fragen: antworte() wird durch eine Attrappe ersetzt."""
from fastapi.testclient import TestClient

import shopfix.web
from shopfix.bot import Antwort

client = TestClient(shopfix.web.app)


def test_chat_gibt_status_und_antwort(monkeypatch):
    monkeypatch.setattr(shopfix.web, "antworte", lambda text: Antwort("ok", "Testantwort"))
    r = client.post("/chat", json={"nachricht": "Wie lange dauert der Versand?"})
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "antwort": "Testantwort"}


def test_leere_nachricht_wird_abgewiesen():
    assert client.post("/chat", json={"nachricht": ""}).status_code == 422


def test_riesige_nachricht_wird_abgewiesen():
    assert client.post("/chat", json={"nachricht": "x" * 20_001}).status_code == 422


def test_seite_zeigt_antwort_als_text():
    r = client.get("/")
    assert "ShopFix Support" in r.text
    assert "textContent" in r.text and "innerHTML" not in r.text
