from src.calculator import Laskija

def test_laskin_laskee_kaksi_perakkaista_oikein():
    laskin = Laskija()
    tulos1 = laskin.laske(2, 3) # 5
    tulos2 = laskin.laske(tulos1, 5) # 10
    assert tulos2 == 10