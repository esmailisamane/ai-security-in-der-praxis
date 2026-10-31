from shopfix.gutschein import Person, freigeben
from shopfix.prompt import SYSTEM


def test_kunde_bekommt_keinen_gutschein_egal_was_er_schreibt():
    assert not freigeben(Person("Kiwi-Fan", "kunde"), 10)


def test_team_bis_zur_grenze():
    team = Person("Support", "team")
    assert freigeben(team, 15)
    assert not freigeben(team, 16)
    assert not freigeben(team, 0)


def test_im_prompt_steht_kein_geheimnis():
    assert "4417" not in SYSTEM and "Freigabe-Code" not in SYSTEM
