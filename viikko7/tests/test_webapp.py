from webapp import create_app
from web_engine import WIN_TARGET


def test_web_flow_human_vs_human_reaches_end():
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY="test")

    client = app.test_client()

    r = client.get("/")
    assert r.status_code == 200

    r = client.post("/new", data={"game_type": "a"}, follow_redirects=False)
    assert r.status_code == 302

    # Pelaa WIN_TARGET voittoa ekalle
    for _ in range(WIN_TARGET):
        r = client.post(
            "/play",
            data={"ekan_siirto": "k", "tokan_siirto": "s"},
            follow_redirects=False,
        )
        assert r.status_code == 200

    html = r.data.decode("utf-8")
    assert "Peli päättyi" in html


def test_reset_clears_session():
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY="test")

    client = app.test_client()

    client.post("/new", data={"game_type": "a"})
    r = client.post("/reset", follow_redirects=False)
    assert r.status_code == 302

    r = client.get("/play", follow_redirects=False)
    assert r.status_code == 302
