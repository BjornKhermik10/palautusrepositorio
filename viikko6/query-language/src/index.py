from statistics import Statistics
from player_reader import PlayerReader
from matchers import And, HasAtLeast, PlaysIn, Not, HasFewerThan, All, Or
# TUO UUSI RAKENTAJA
from query_builder import QueryBuilder 

def main():
    url = "https://studies.cs.helsinki.fi//nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    print("--- Testi 1: Kaikki pelaajat (tyhjä kysely) ---")
    query1 = QueryBuilder()
    matcher1 = query1.build()
    
    # Tarkistetaan, että kaikki pelaajat palautetaan
    print(f"Pelaajien kokonaisluku: {len(stats.matches(matcher1))}\n")


    print("--- Testi 2: NYR pelaajat ---")
    query2 = QueryBuilder()
    matcher2 = query2.plays_in("NYR").build()

    for player in stats.matches(matcher2):
        # Tulostaa kaikki NYR pelaajat
        # print(player)
        pass # Kommentoidaan pois, ettei tuloste ole liian pitkä


    print("\n--- Testi 3: NYR, 10 <= maalit < 20 ---")
    query3 = QueryBuilder()

    print("\n--- Testi 4: PHILADELPHIA (apu < 10 maalia) TAI EDMONTON (apu >= 50 pistettä) ---")
    
    # Luo päärakentaja
    query = QueryBuilder()

    # Kyselyn toteutus one_of-metodilla
    matcher = (
        query
        .one_of(
            # Alikysely 1: PHI, väh. 10 syöttöä, alle 10 maalia
            QueryBuilder()
                .plays_in("PHI")
                .has_at_least(10, "assists")
                .has_fewer_than(10, "goals"),
            
            # Alikysely 2: EDM, väh. 50 pistettä
            QueryBuilder()
                .plays_in("EDM")
                .has_at_least(50, "points")
        )
        .build()
    )
    
    for player in stats.matches(matcher):
        print(player)
        
if __name__ == "__main__":
    main()
