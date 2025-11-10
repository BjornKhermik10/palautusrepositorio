"""Module for reading NHL player data and displaying stats."""

import requests
from rich.console import Console
from rich.table import Table
from rich.text import Text
from player import Player

# pylint: disable=too-few-public-methods
class PlayerReader:
    """Reads player data from a given URL."""

    def __init__(self, url: str):
        """Initialize with URL."""
        self.url = url
        self._players = None

    def get_players(self):
        """Return a list of Player objects from the API."""
        if self._players is None:
            response = requests.get(self.url, timeout=10).json()
            self._players = [Player(p) for p in response]
        return self._players


# pylint: disable=too-few-public-methods
class PlayerStats:
    """Provides stats for a list of players."""

    def __init__(self, reader: PlayerReader):
        """Initialize with a PlayerReader."""
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality: str):
        """Return players filtered by nationality, sorted by points."""
        filtered = [p for p in self.players if p.nationality.upper() == nationality.upper()]
        return sorted(filtered, key=lambda p: p.points, reverse=True)


def main():
    """Main function for running the NHL stats viewer."""
    console = Console()

    season = console.input("Enter season (e.g., 2024-25): ")
    nationality = console.input("Enter nationality code (e.g., FIN): ").upper()

    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)

    if not players:
        console.print(f"[bold red]No players found for {nationality} in season {season}[/bold red]")
        return

    title_text = Text(f"Players from {nationality} in {season}", style="bold magenta")
    table = Table(title=title_text)

    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Team", style="green")
    table.add_column("Goals", justify="right", style="yellow")
    table.add_column("Assists", justify="right", style="yellow")
    table.add_column("Points", justify="right", style="bright_magenta")

    for player in players:
        table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.points))

    console.print(table)


if __name__ == "__main__":
    main()
