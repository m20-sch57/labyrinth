from labyrinth_engine.labyrinth_object import LabyrinthObject
from labyrinth_engine.lr_types import Location, Item, Player, Creature
from labyrinth_engine.ui_buttons import Button
from labyrinth_engine.ui_status_bars import Bar

from typing import Any, Dict, Union, List, Callable, Set


class Labyrinth:
    def __init__(self,
                 locations: List[Location],
                 items: List[Item],
                 creatures: List[Creature],
                 players: List[Player],
                 adjacence_list: Dict,
                 settings,
                 imagepath: str,
                 seed: Union[int, Any],
                 loadseed: Union[int, Any]) -> None:

        self.seed = ... # type: Union[int, Any]
        self.loadseed = ... # type: Union[int, Any]
        self.imagepath = ... # type: str

        self.unique_objects = ... # type: Dict[str, LabyrinthObject]

        self.locations = ... # type: Set[Location]
        self.items = ... # type: Set[Item]
        self.creatures = ... # type: Set[Creature]
        self.players_list = ... # type: List[Player]

        self.to_send = ... # type: Dict[int, Dict[str, List[str]]]
        self.active_player_number = ... # type: int
        self.is_game_ended = ... # type: bool

        self.turns_log = ... # type: List[Dict[str, str]]
        self.msgs_log = ... # type: Dict[str, List[str]]

        self.MAX_COUNT_OF_SKIPS = ... # type: int

    # Сообщения.
    def send_msg(self, msg: str, player: Player, priority: int = 0) -> None: ...
    def clear_to_send(self) -> Dict[int, Dict[str, List[str]]]: ...
    def regularize_to_send(self) -> Dict[str, List[str]]: ...
    def player_to_send(self, username: str) -> List[str]: ...
    def get_msgs(self, username: str) -> List[str]: ...

    # Уникальные предметы.
    def set_unique(self, obj: LabyrinthObject, key: str) -> None: ...
    def get_unique(self, key: str) -> LabyrinthObject: ...

    # Ход игрока.
    def make_turn(self, turn: str) -> Dict[str, List[str]]: ...
    def skip_turn(self) -> None: ...
    def get_turns(self, number: Union[int, None] = None, username: Union[str, None] = None) -> Union[List[str], str]: ...
    def end_game(self) -> None: ...

    # Активный игрок.
    def get_next_active_player_number(self) -> Union[None, int]: ...
    def get_next_active_player(self) -> Union[None, Player]: ...
    def get_active_player(self) -> Player: ...
    def get_active_player_username(self) -> str: ...
    def get_active_player_ats(self) -> List[str]: ...

    # Объекты Лабиринта.
    def get_all_objects(self) -> Set[LabyrinthObject]: ...
    def get_objects(self,
                    lrtype: Union[str, List[str]] = ['location', 'item', 'player', 'creature'],
                    class_names: Union[str, List[str]] = [],
                    flags: List[str] = [],
                    key: Callable[[LabyrinthObject], bool] = lambda x: True): ...

    def save(self) -> str: ...

    def get_buttons(self) -> List[Button]: ...

    def get_bars(self, username: str) -> List[Bar]: ...
