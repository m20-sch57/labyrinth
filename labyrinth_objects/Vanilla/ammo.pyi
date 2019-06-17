from labyrinth_engine.ui_status_bars import StringBar
from labyrinth_engine import Location, Item, Player, Creature

from typing import Any, Dict, Union, List, Callable


class Ammo(Item):
    def __init__(self):
        self.bullet_counter_bar = ... # type: StringBar
        self.bomb_counter_bar = ... # type: StringBar

    def update_bars(self) -> None: ...

    def set_settings(self,
                     settings: Dict[str, Any],
                     locations: List[Location],
                     items: List[Item],
                     creatures: List[Creature],
                     players: List[Player]):

        self.MAX_BULLETS_COUNT = ... # type: int
        self.MAX_BOMBS_COUNT = ... # type: int

        self.INIT_BULLETS_COUNT = ... # type: int
        self.INIT_BOMBS_COUNT = ... # type: int

        self.bullets = ... # type: Dict[Player, ]
        self.bombs = ... # type: Dict[Player, ]

    def spend(self, ammo_type: str, player):
        if ammo_type == 'bullet':
            self.bullets[player] -= 1
            self.update_bars()
            return self.bullets[player]
        elif ammo_type == 'bomb':
            self.bombs[player] -= 1
            self.update_bars()
            return self.bombs[player]

    def have(self, ammo_type: str, player: Player) -> bool: ...
    def reset(self, ammo_type: str, player: Player) -> None: ...
    def reset_all(self, player: Player) -> None: ...
