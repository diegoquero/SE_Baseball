from dataclasses import dataclass
@dataclass

class Appearance:
    id : int
    year :int
    team_code: str
    team_id : int
    player_id : int
    games : int
    games_started: int
    games_batting: int
    games_defense: int
    games_pitcher: int
    games_catcher: int

    def __hash__(self):
        return hash(self.id)