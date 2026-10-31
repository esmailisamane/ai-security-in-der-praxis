from shopfix.messen import quote, wilson


def test_wilson_bekannte_werte():
    # 0 von 10 heißt nicht "nie": bis knapp 28 % sind noch plausibel
    assert round(wilson(0, 10)[1], 3) == 0.278
    assert round(wilson(10, 10)[0], 3) == 0.722


def test_ein_lauf_sagt_fast_nichts():
    unten, oben = wilson(1, 1)
    assert unten < 0.25 and oben == 1.0


def test_quote_text():
    assert quote(96, 100) == "96 von 100 = 96 % (95 %-Bereich: 90 % bis 98 %)"
