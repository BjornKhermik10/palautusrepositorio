class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False

        return True


class PlaysIn:
    def __init__(self, team):
        self._team = team

    def test(self, player):
        return player.team == self._team


class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)
        return player_value >= self._value

class All:
    def test(self, player):
        return True

class Not:
    def __init__(self, condition):
        self._condition = condition

    def test(self, player):
        return not self._condition.test(player)

class HasFewerThan:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)
        return player_value < self._value
    
class Or:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        # Käydään läpi kaikki ehdot.
        for matcher in self._matchers:
            # Jos yksikin ehto palauttaa True, Or-ehto on täytetty.
            if matcher.test(player):
                return True
        
        # Jos yksikään ehdoista ei palauttanut True, palautetaan False.
        return False
