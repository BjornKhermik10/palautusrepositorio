from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Optional

from kivi_paperi_sakset import KiviPaperiSakset
from peli_tehdas import luo_peli
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from tuomari import Tuomari

GameType = Literal["a", "b", "c"]

WIN_TARGET = 3


@dataclass(frozen=True)
class RoundResult:
    ekan_siirto: str
    tokan_siirto: str
    voittaja: Literal["eka", "toka", "tasapeli"]
    tilanne: str
    paattyi: bool
    virhe: Optional[str] = None


def kierroksen_voittaja(ekan_siirto: str, tokan_siirto: str) -> Literal["eka", "toka", "tasapeli"]:
    if ekan_siirto == tokan_siirto:
        return "tasapeli"
    if (ekan_siirto == "k" and tokan_siirto == "s") or (
        ekan_siirto == "s" and tokan_siirto == "p"
    ) or (ekan_siirto == "p" and tokan_siirto == "k"):
        return "eka"
    return "toka"


def _validator() -> KiviPaperiSakset:
    return KiviPaperiSakset()


def onko_ok_siirto(siirto: str) -> bool:
    return _validator()._onko_ok_siirto(siirto)


def new_state(game_type: GameType) -> dict[str, Any]:
    peli = luo_peli(game_type)
    if peli is None:
        raise ValueError(f"Tuntematon pelityyppi: {game_type}")

    state: dict[str, Any] = {
        "game_type": game_type,
        "ended": False,
        "tuomari": {"ekan": 0, "tokan": 0, "tasapelit": 0},
        "ai": None,
        "last": None,
    }

    if game_type == "b":
        state["ai"] = {"kind": "tekoaly", "_siirto": 0}
    elif game_type == "c":
        state["ai"] = {
            "kind": "tekoaly_parannettu",
            "_muisti": [None] * 10,
            "_vapaa_muisti_indeksi": 0,
        }

    return state


def _tuomari_from_state(state: dict[str, Any]) -> Tuomari:
    t = Tuomari()
    tuomari_state = state.get("tuomari") or {}
    t.ekan_pisteet = int(tuomari_state.get("ekan", 0))
    t.tokan_pisteet = int(tuomari_state.get("tokan", 0))
    t.tasapelit = int(tuomari_state.get("tasapelit", 0))
    return t


def _save_tuomari(state: dict[str, Any], tuomari: Tuomari) -> None:
    state["tuomari"] = {
        "ekan": tuomari.ekan_pisteet,
        "tokan": tuomari.tokan_pisteet,
        "tasapelit": tuomari.tasapelit,
    }


def _ai_from_state(state: dict[str, Any]) -> Optional[object]:
    ai_state = state.get("ai")
    if not ai_state:
        return None

    if ai_state.get("kind") == "tekoaly":
        ai = Tekoaly()
        ai._siirto = int(ai_state.get("_siirto", 0))
        return ai

    if ai_state.get("kind") == "tekoaly_parannettu":
        ai = TekoalyParannettu(len(ai_state.get("_muisti", [])) or 10)
        ai._muisti = list(ai_state.get("_muisti", [None] * 10))
        ai._vapaa_muisti_indeksi = int(ai_state.get("_vapaa_muisti_indeksi", 0))
        return ai

    return None


def _save_ai(state: dict[str, Any], ai: object) -> None:
    if isinstance(ai, Tekoaly):
        state["ai"] = {"kind": "tekoaly", "_siirto": ai._siirto}
        return

    if isinstance(ai, TekoalyParannettu):
        state["ai"] = {
            "kind": "tekoaly_parannettu",
            "_muisti": list(ai._muisti),
            "_vapaa_muisti_indeksi": ai._vapaa_muisti_indeksi,
        }
        return


def _normalize_move(value: Optional[str]) -> str:
    return (value or "").strip().lower()


def play_round(
    state: dict[str, Any],
    ekan_siirto_raw: Optional[str],
    tokan_siirto_raw: Optional[str] = None,
) -> tuple[dict[str, Any], RoundResult]:
    if state.get("ended"):
        return state, RoundResult("", "", "tasapeli", str(_tuomari_from_state(state)), True, "Peli on jo päättynyt.")

    game_type: GameType = state.get("game_type")
    ekan_siirto = _normalize_move(ekan_siirto_raw)
    tokan_siirto = _normalize_move(tokan_siirto_raw)

    if not onko_ok_siirto(ekan_siirto):
        state["ended"] = True
        t = _tuomari_from_state(state)
        return state, RoundResult(ekan_siirto, "", "tasapeli", str(t), True, "Virheellinen siirto. Peli päättyi.")

    tuomari = _tuomari_from_state(state)

    if game_type == "a":
        if not onko_ok_siirto(tokan_siirto):
            state["ended"] = True
            return state, RoundResult(
                ekan_siirto,
                tokan_siirto,
                "tasapeli",
                str(tuomari),
                True,
                "Virheellinen siirto. Peli päättyi.",
            )

    if game_type in ("b", "c"):
        ai = _ai_from_state(state)
        if ai is None:
            state["ended"] = True
            return state, RoundResult(
                ekan_siirto,
                "",
                "tasapeli",
                str(tuomari),
                True,
                "Tekoälyn tila puuttuu. Peli päättyi.",
            )
        tokan_siirto = ai.anna_siirto()  # type: ignore[attr-defined]

    if not onko_ok_siirto(tokan_siirto):
        state["ended"] = True
        return state, RoundResult(
            ekan_siirto,
            tokan_siirto,
            "tasapeli",
            str(tuomari),
            True,
            "Virheellinen siirto. Peli päättyi.",
        )

    tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)

    voittaja = kierroksen_voittaja(ekan_siirto, tokan_siirto)

    if tuomari.ekan_pisteet >= WIN_TARGET or tuomari.tokan_pisteet >= WIN_TARGET:
        state["ended"] = True

    if game_type == "c":
        ai = _ai_from_state(state)
        if ai is not None:
            ai.aseta_siirto(ekan_siirto)  # type: ignore[attr-defined]
            _save_ai(state, ai)

    if game_type == "b":
        ai = _ai_from_state(state)
        if ai is not None:
            _save_ai(state, ai)

    _save_tuomari(state, tuomari)
    state["last"] = {"ekan": ekan_siirto, "tokan": tokan_siirto, "voittaja": voittaja}

    return state, RoundResult(
        ekan_siirto,
        tokan_siirto,
        voittaja,
        str(tuomari),
        bool(state.get("ended")),
        None,
    )
