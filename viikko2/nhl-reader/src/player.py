"""Module representing a NHL player."""

# pylint: disable=too-few-public-methods
class Player:
    """Represents a NHL player with stats."""

    def __init__(self, data: dict):
        """Initialize player attributes from a data dictionary."""
        self.name = data.get("name", "")
        self.team = data.get("team", "")
        self.goals = data.get("goals", 0)
        self.assists = data.get("assists", 0)
        self.nationality = data.get("nationality", "")
        self.points = self.goals + self.assists

    def __str__(self):
        """Return a string representation of the player."""
        return f"{self.name:20} {self.team:15} {self.goals} + {self.assists} = {self.points}"
