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

        # Palautetaan oletuksena viite 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        # Määritellään sivuvaikutus (side_effect) varaston saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 10
            if tuote_id == 3:
                return 0
            return 0

        # Määritellään sivuvaikutus varaston hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "piimä", 4)
            if tuote_id == 3:
                return Tuote(3, "leipä", 6)
            return None

        # Kytketään sivuvaikutukset mock-olioon
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # Alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    # --- TEHTÄVÄ 3 TESTIT ---

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_kaksi_eri_tuotetta_tilisiirto_kutsutaan_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 9)

    def test_kaksi_samaa_tuotetta_tilisiirto_kutsutaan_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 10)

    def test_tuote_loppu_tilisiirto_kutsutaan_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3) # Loppu
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    # --- TEHTÄVÄ 4 UUDET TESTIT ---

    # 1. Varmistetaan, että aloita_asiointi nollaa edelliset tiedot
    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1) # Hinta 5
        
        # Aloitetaan uusi asiointi, ostoskorin pitäisi tyhjentyä
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2) # Hinta 4
        
        self.kauppa.tilimaksu("pekka", "12345")
        
        # Odotetaan summaa 4 (vain jälkimmäinen ostos), ei 9
        self.pankki_mock.tilisiirto.assert_called_with(ANY, ANY, ANY, ANY, 4)

    # 2. Varmistetaan, että uusi viitenumero pyydetään joka kerta
    def test_kauppa_pyytaa_uuden_viitenumeron_jokaiselle_maksutapahtumalle(self):
        # Määritellään, että viitegeneraattori palauttaa järjestyksessä 42, 43, 44
        self.viitegeneraattori_mock.uusi.side_effect = [42, 43, 44]

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        
        # Ensimmäinen maksu, viite 42
        self.pankki_mock.tilisiirto.assert_called_with(ANY, 42, ANY, ANY, ANY)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # Toinen maksu, viite 43
        self.pankki_mock.tilisiirto.assert_called_with(ANY, 43, ANY, ANY, ANY)

    # 3. Testataan poistamista (Coveragen nosto 100%:iin)
    def test_poista_korista_palauttaa_varastoon(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1) # Lisätään maito (5e)
        self.kauppa.poista_korista(1) # Poistetaan maito
        
        self.kauppa.tilimaksu("pekka", "12345")

        # Summan pitäisi olla 0, koska tuote poistettiin
        self.pankki_mock.tilisiirto.assert_called_with(ANY, ANY, ANY, ANY, 0)
        
        # Varmistetaan myös, että varastoon palautus -metodia kutsuttiin
        self.varasto_mock.palauta_varastoon.assert_called()