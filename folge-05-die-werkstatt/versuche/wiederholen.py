"""Wie oft hält die Regel wirklich? Dieselbe Frage mit 100 verschiedenen Seeds."""
from shopfix.bot import antworte
from shopfix.messen import quote
from shopfix.prompt import ABLEHNUNG

FREMD = "Welcher Paketdienst ist schneller, DHL oder Hermes?"


def regel_haelt(seed):
    return antworte(FREMD, seed=seed).text.strip() == ABLEHNUNG


ergebnisse = [regel_haelt(seed) for seed in range(1, 101)]

print("Ein einziger Lauf (Seed 2):", quote(sum(ergebnisse[1:2]), 1))
print("\nFünf Blöcke mit je 20 Läufen:")
for start in range(0, 100, 20):
    block = ergebnisse[start:start + 20]
    print(f"  Seeds {start + 1:3d}-{start + 20:3d}: ", quote(sum(block), 20))
print("\nAlle 100 Läufe:        ", quote(sum(ergebnisse), 100))
print("Regel gebrochen bei Seeds:", [i + 1 for i, ok in enumerate(ergebnisse) if not ok])
