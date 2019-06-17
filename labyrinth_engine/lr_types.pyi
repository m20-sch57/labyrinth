from labyrinth_engine import LabyrinthObject as LO

from typing import Any, Dict


class Location(LO):
    _lrtype = ... # type: str

    def __init__(self) -> None:
        self.directions = ... # type: Dict[str, Location]

    def get_neighbour(self, direction: str) -> Location: ...

    def set_neighbour(self, direction: str, neighbour: Location) -> Any: ...


class Item(LO):
    _lrtype = ... # type: str


class Player(LO):
    _lrtype = ... # type: str

    def __init__(self, username: str):
        self.name = self.username = ... # type: str

    def get_username(self) -> str: ...

    def set_turns_skip(self, count: int) -> None: ...

    def add_turns_skip(self, count: int) -> None: ...

    def die(self) -> None: ...

    def revive(self) -> None: ...


class Creature(LO):
    _lrtype = ... # type: str
