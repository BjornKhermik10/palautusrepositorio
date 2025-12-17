from web_engine import WIN_TARGET, new_state, play_round


def test_game_ends_when_first_reaches_win_target():
    state = new_state("a")

    # eka voittaa aina: k vs s
    for i in range(WIN_TARGET):
        state, result = play_round(state, "k", "s")
        assert result.virhe is None
        assert state["tuomari"]["ekan"] == i + 1

    assert state["ended"] is True


def test_invalid_move_ends_game_immediately():
    state = new_state("a")
    state, result = play_round(state, "x", "k")

    assert state["ended"] is True
    assert result.virhe is not None


def test_ai_game_progresses_and_ends_by_win_target():
    state = new_state("b")

    # tekoäly antaa deterministisesti siirtoja k,p,s... alkaen p (koska _siirto kasvaa)
    # pelataan niin, että ekalla on mahdollisuus voittaa useammin kuin hävitä.
    # Käytetään eka: p niin, että se voittaa kiviä vastaan.
    while not state["ended"]:
        state, result = play_round(state, "p")
        assert result.virhe is None

    assert state["tuomari"]["ekan"] >= 0
    assert state["tuomari"]["tokan"] >= 0
    assert state["tuomari"]["ekan"] == WIN_TARGET or state["tuomari"]["tokan"] == WIN_TARGET
