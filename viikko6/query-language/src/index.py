from statistics import Statistics
from player_reader import PlayerReader
from matchers import And, HasAtLeast, PlaysIn, Not, HasFewerThan, All, Or
# TUO UUSI RAKENTAJA
from query_builder import QueryBuilder 

def main():
    url = "https://studies.cs.helsinki.fi//nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    # ... (edelliset testit)

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