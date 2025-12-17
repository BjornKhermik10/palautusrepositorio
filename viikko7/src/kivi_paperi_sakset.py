from tuomari import Tuomari

class KiviPaperiSakset:
    def pelaa(self):
        tuomari = Tuomari()

        while True:
            ekan_siirto = self._ensimmaisen_siirto()
            tokan_siirto = self._toisen_siirto(ekan_siirto)

            if not self._onko_ok_siirto(ekan_siirto) or not self._onko_ok_siirto(tokan_siirto):
                break

            tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(tuomari)

        print("Kiitos!")
        print(tuomari)

    def _ensimmaisen_siirto(self):
        return input("Ensimmäisen pelaajan siirto: ")

    def _onko_ok_siirto(self, siirto):
        return siirto in ["k", "p", "s"]

    def _toisen_siirto(self, ensimmaisen_siirto):
        raise NotImplementedError("Tämä metodi pitää korvata aliluokassa")