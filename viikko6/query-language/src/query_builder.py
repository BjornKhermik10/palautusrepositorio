from matchers import And, PlaysIn, HasAtLeast, HasFewerThan, All, Or

class QueryBuilder:
    def __init__(self, matcher=None):
        # Sallitaan Matcher-olion asettaminen alussa, 
        # mikä on tarpeen toistuvien alikyselyjen (recursiveness) yhteydessä.
        if matcher:
            self._matcher = matcher
        else:
            self._matcher = All() 

    def plays_in(self, team):
        self._matcher = And(self._matcher, PlaysIn(team))
        return self

    def has_at_least(self, value, attr):
        self._matcher = And(self._matcher, HasAtLeast(value, attr))
        return self

    def has_fewer_than(self, value, attr):
        self._matcher = And(self._matcher, HasFewerThan(value, attr))
        return self
    
    # --- UUSI OR-LOGIIKKA ---

    def one_of(self, *queries):
        # 1. Kerää kaikki alikyselyjen Matcher-oliot listaan
        matchers_from_queries = []
        
        # Koska *queries sisältää QueryBuilder-olioita, meidän on 'rakennettava' ne:
        for query in queries:
            # Käytämme QueryBuilderin build()-metodia poimimaan Matcher-olion
            matchers_from_queries.append(query.build())
            
        # 2. Luo uusi Or-matcher kaikista kerätyistä Matchereista
        or_matcher = Or(*matchers_from_queries)
        
        # 3. Yhdistä uusi Or-matcher nykyiseen pääkyselyyn And-periaatteella
        self._matcher = And(self._matcher, or_matcher)
        
        # 4. Palautetaan itse rakentaja ketjutusta varten
        return self
        
    # -------------------------

    def build(self):
        # Palauttaa rakennetun Matcher-olion.
        return self._matcher