from __future__ import annotations

import os
from typing import Optional

from flask import Flask, redirect, render_template, request, session, url_for

from web_engine import WIN_TARGET, GameType, new_state, play_round


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

    @app.get("/")
    def index():
        current = session.get("kps")
        return render_template("index.html", current=current, win_target=WIN_TARGET)

    @app.post("/new")
    def start_new():
        game_type: Optional[str] = request.form.get("game_type")
        if game_type not in ("a", "b", "c"):
            return redirect(url_for("index"))

        session["kps"] = new_state(game_type)  # type: ignore[arg-type]
        return redirect(url_for("play"))

    @app.get("/play")
    def play():
        state = session.get("kps")
        if not state:
            return redirect(url_for("index"))

        game_type: GameType = state.get("game_type")
        ended = bool(state.get("ended"))
        last = state.get("last")
        tuomari = state.get("tuomari")

        return render_template(
            "play.html",
            game_type=game_type,
            ended=ended,
            last=last,
            tuomari=tuomari,
            win_target=WIN_TARGET,
            error=None,
        )

    @app.post("/play")
    def play_post():
        state = session.get("kps")
        if not state:
            return redirect(url_for("index"))

        game_type: GameType = state.get("game_type")
        ekan = request.form.get("ekan_siirto")
        tokan = request.form.get("tokan_siirto")

        state, result = play_round(state, ekan, tokan)
        session["kps"] = state

        return render_template(
            "play.html",
            game_type=game_type,
            ended=bool(state.get("ended")),
            last=state.get("last"),
            tuomari=state.get("tuomari"),
            win_target=WIN_TARGET,
            error=result.virhe,
        )

    @app.post("/reset")
    def reset():
        session.pop("kps", None)
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
