from enum import Enum
from tkinter import ttk, constants, StringVar
from abc import ABC, abstractmethod

# Oletetaan että Sovelluslogiikka on tuotu oikein
# from sovelluslogiikka import Sovelluslogiikka

class Komento(Enum):
    SUMMA = 1
    EROTUS = 2
    NOLLAUS = 3
    KUMOA = 4

# --- Komento-oliot ---

class AbstraktiKomento(ABC):
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen_arvo = 0 # Tähän tallennetaan tila ennen suoritusta

    @abstractmethod
    def suorita(self):
        pass

    def kumoa(self):
        """Palauttaa sovelluslogiikan tilan ennen komennon suoritusta."""
        self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)

class Summa(AbstraktiKomento):
    def suorita(self):
        # 1. Talletetaan nykyinen arvo ennen muutosta
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        
        # 2. Suoritetaan laskutoimitus
        try:
            arvo = int(self._lue_syote())
        except Exception:
            arvo = 0
        
        self._sovelluslogiikka.plus(arvo)

class Erotus(AbstraktiKomento):
    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        try:
            arvo = int(self._lue_syote())
        except Exception:
            arvo = 0

        self._sovelluslogiikka.miinus(arvo)

class Nollaus(AbstraktiKomento):
    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.nollaa()

# Huom: Kumoa ei ole enää tavallinen komento-olio, vaan sitä käsitellään erikseen käyttöliittymässä.

# --- Käyttöliittymä ---

class Kayttoliittyma:
    def __init__(self, sovelluslogiikka, root):
        self._sovelluslogiikka = sovelluslogiikka
        self._root = root
        
        # BONUSTEHTÄVÄN VAATIMUS:
        # Jotta voimme kumota useita askeleita, meidän täytyy luoda uusi olio
        # jokaista painallusta kohden. Siksi sanakirjassa on nyt LUOKAT eikä oliot.
        self._komennot = {
            Komento.SUMMA: Summa,
            Komento.EROTUS: Erotus,
            Komento.NOLLAUS: Nollaus
        }
        
        # Lista suoritetuista komennoista (historia)
        self._komento_historia = []

    def kaynnista(self):
        self._arvo_var = StringVar()
        self._arvo_var.set(self._sovelluslogiikka.arvo())
        self._syote_kentta = ttk.Entry(master=self._root)

        tulos_teksti = ttk.Label(textvariable=self._arvo_var)

        summa_painike = ttk.Button(
            master=self._root,
            text="Summa",
            command=lambda: self._suorita_komento(Komento.SUMMA)
        )

        erotus_painike = ttk.Button(
            master=self._root,
            text="Erotus",
            command=lambda: self._suorita_komento(Komento.EROTUS)
        )

        self._nollaus_painike = ttk.Button(
            master=self._root,
            text="Nollaus",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.NOLLAUS)
        )

        self._kumoa_painike = ttk.Button(
            master=self._root,
            text="Kumoa",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.KUMOA)
        )

        tulos_teksti.grid(columnspan=4)
        self._syote_kentta.grid(columnspan=4, sticky=(constants.E, constants.W))
        summa_painike.grid(row=2, column=0)
        erotus_painike.grid(row=2, column=1)
        self._nollaus_painike.grid(row=2, column=2)
        self._kumoa_painike.grid(row=2, column=3)
    
    def _lue_syote(self):
        return self._syote_kentta.get()

    def _suorita_komento(self, komento):
        if komento == Komento.KUMOA:
            # KUMOA-TOIMINNALLISUUS
            if len(self._komento_historia) > 0:
                # 1. Otetaan listasta viimeisin komento-olio
                viimeisin_komento = self._komento_historia.pop()
                # 2. Kutsutaan sen kumoa-metodia
                viimeisin_komento.kumoa()

        elif komento in self._komennot:
            # TAVALLINEN KOMENTO (Summa, Erotus, Nollaus)
            
            # 1. Haetaan luokka sanakirjasta
            komento_luokka = self._komennot[komento]
            
            # 2. Luodaan uusi olio tästä luokasta
            komento_olio = komento_luokka(self._sovelluslogiikka, self._lue_syote)
            
            # 3. Suoritetaan komento
            komento_olio.suorita()
            
            # 4. Lisätään suoritettu olio historiaan
            self._komento_historia.append(komento_olio)

        # KÄYTTÖLIITTYMÄN PÄIVITYS
        
        # Kumoa-nappi on aktiivinen vain, jos historiassa on komentoja
        if len(self._komento_historia) > 0:
            self._kumoa_painike["state"] = constants.NORMAL
        else:
            self._kumoa_painike["state"] = constants.DISABLED

        if self._sovelluslogiikka.arvo() == 0:
            self._nollaus_painike["state"] = constants.DISABLED
        else:
            self._nollaus_painike["state"] = constants.NORMAL

        self._syote_kentta.delete(0, constants.END)
        self._arvo_var.set(self._sovelluslogiikka.arvo())