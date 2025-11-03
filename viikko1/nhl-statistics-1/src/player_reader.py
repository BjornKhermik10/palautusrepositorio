import urllib.request
import json
from player import Player

class PlayerReader:
    def __init__(self, url):
        self.url = url

    def get_players(self):
        response = urllib.request.urlopen(self.url)
        content = response.read()
        players_dict = json.loads(content)

        players = []

        for player in players_dict:
            players.append(
                Player(
                    player["name"],
                    player["team"],
                    player["goals"],
                    player["assists"]
                )
            )

        return players