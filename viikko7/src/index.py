from peli_tehdas import luo_peli

def main():
    while True:
        print("Valitse pelataanko"
              "\n (a) Ihmistä vastaan"
              "\n (b) Tekoälyä vastaan"
              "\n (c) Parannettua tekoälyä vastaan"
              "\nMuilla valinnoilla lopetetaan"
        )

        vastaus = input()
        peli = luo_peli(vastaus)

        if peli:
            print("Peli alkaa. Pelin voi lopettaa syöttämällä jotain muuta kuin k, p tai s.")
            peli.pelaa()
        else:
            break

if __name__ == "__main__":
    main()