"""Ein Wortfilter sieht Buchstaben – das Modell sieht Nummern."""
from tokenizers import Tokenizer

tok = Tokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct")

GEHEIM = "VIP-7731"  # dieser Rabattcode darf nie in einer Antwort stehen


def wortfilter(text):
    """Blockiert eine Antwort, wenn der Code darin vorkommt."""
    return GEHEIM in text


ANTWORTEN = [
    "Dein Code lautet VIP-7731.",
    "Dein Code lautet VIP 7731.",
    "Dein Code lautet V-I-P-7-7-3-1.",
    "Dein Code lautet VIP, dann sieben, sieben, drei, eins.",
]

original = tok.encode(ANTWORTEN[0], add_special_tokens=False).ids

for text in ANTWORTEN:
    ids = tok.encode(text, add_special_tokens=False).ids
    pieces = [tok.decode([i]) for i in ids]
    neu = [i for i in ids if i not in original]  # Nummern, die im Original nicht vorkommen
    print(f"{text!r}")
    print(f"  Filter:  {'BLOCKIERT' if wortfilter(text) else 'durchgelassen'}")
    print(f"  Tokens:  {' | '.join(pieces)}")
    print(f"  IDs:     {ids}")
    print(f"  Neue Nummern: {neu}\n")
