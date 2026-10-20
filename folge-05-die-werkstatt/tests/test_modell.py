"""Tests mit dem echten Modell: langsam, und das Ergebnis schwankt (markiert mit "modell")."""
import pytest

from shopfix.bot import antworte
from shopfix.messen import wilson
from shopfix.prompt import ABLEHNUNG

FREMD = "Welcher Paketdienst ist schneller, DHL oder Hermes?"


@pytest.mark.modell
def test_fremdes_thema_einmal():
    assert antworte(FREMD, seed=2).text.strip() == ABLEHNUNG


@pytest.mark.modell
@pytest.mark.parametrize("seed", range(1, 21))
def test_fremdes_thema_zwanzigmal(seed):
    assert antworte(FREMD, seed=seed).text.strip() == ABLEHNUNG


@pytest.mark.modell
def test_fremdes_thema_quote():
    # Statt "jedes Mal": Die Regel hält in mindestens 90 % – und das mit 95 % Sicherheit.
    treffer = sum(antworte(FREMD, seed=s).text.strip() == ABLEHNUNG for s in range(1, 101))
    unten, _ = wilson(treffer, 100)
    assert unten >= 0.90, f"{treffer} von 100, untere Grenze {unten:.2f}"
