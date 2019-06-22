from labyrinth_engine import LabyrinthObject as LO

from typing import Any, Dict, TypeVar


class Location(LO):
    directions: Dict[str, AnyLocation]

    def get_neighbour(self, direction: str) -> AnyLocation: ...

    def set_neighbour(self, direction: str, neighbour: AnyLocation) -> Any: ...

AnyLocation = TypeVar('AnyLocation', bound=Location)


class Item(LO):  ...

AnyItem = TypeVar('AnyItem', bound=Item)


class Player(LO):
    name: str
    username: str

    def __init__(self, username: str): ...

    def get_username(self) -> str: ...

    def set_turns_skip(self, count: int) -> None: ...

    def add_turns_skip(self, count: int) -> None: ...

    def die(self) -> None: ...

    def revive(self) -> None: ...

AnyPlayer = TypeVar('AnyPlayer', bound=Player)


class Creature(LO): ...

AnyCreature = TypeVar('AnyCreature', bound=Creature)