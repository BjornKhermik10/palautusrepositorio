import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()

        # Palautetaan aina viite 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        # Määritellään sivuvaikutus (side_effect) varaston saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10  # Maitoa on 10 kpl
            if tuote_id == 2:
                return 10  # Piimää on 10 kpl
            if tuote_id == 3:
                return 0   # Leipä on loppu
            return 0

        # Määritellään sivuvaikutus varaston hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)  # Maito maksaa 5
            if tuote_id == 2:
                return Tuote(2, "piimä", 4)  # Piimä maksaa 4
            if tuote_id == 3:
                return Tuote(3, "leipä", 6)  # Leipä maksaa 6
            return None

        # Kytketään sivuvaikutukset mock-olioon
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # Alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    # TESTI 1: Yksi tuote (Maito, 5e)
    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1) # Lisätään maito (5€)
        self.kauppa.tilimaksu("pekka", "12345")

        # Tarkistetaan argumentit: nimi, viite, asiakkaan tili, kaupan tili, summa
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    # TESTI 2: Kaksi eri tuotetta (Maito 5e + Piimä 4e = 9e)
    def test_kaksi_eri_tuotetta_tilisiirto_kutsutaan_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1) # Maito (5€)
        self.kauppa.lisaa_koriin(2) # Piimä (4€)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 9)

    # TESTI 3: Kaksi samaa tuotetta (Maito 5e + Maito 5e = 10e)
    def test_kaksi_samaa_tuotetta_tilisiirto_kutsutaan_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1) # Maito (5€)
        self.kauppa.lisaa_koriin(1) # Maito (5€)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 10)

    # TESTI 4: Yksi saatavilla, yksi loppu (Maito 5e + Leipä 6e(loppu) = 5e)
    def test_tuote_loppu_tilisiirto_kutsutaan_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1) # Maito (5€) - ONNISTUU
        self.kauppa.lisaa_koriin(3) # Leipä (6€) - LOPPU VARASTOSTA
        self.kauppa.tilimaksu("pekka", "12345")

        # Vain maito pitäisi veloittaa (5€)
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)