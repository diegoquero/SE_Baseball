from dataclasses import dataclass

@dataclass
class Team:
    id : int
    year : int
    team_code : str
    name :str

    def __hash__(self):
        return hash(self.id)