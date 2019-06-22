from labyrinth_engine.labyrinth_object import AnyLO
from labyrinth_engine.lr_types import Location, Item, Player, Creature
from labyrinth_engine.ui_buttons import Button
from labyrinth_engine.ui_status_bars import Bar

from typing import Any, Dict, Union, List, Callable, Set


class Labyrinth:

    seed: Union[int, Any]
    loadseed: Union[int, Any]
    imagepath: str

    unique_objects: Dict[str, AnyLO]

    locations: Set[Location]
    items: Set[Item]
    creatures: Set[Creature]
    players_list: List[Player]

    to_send: Dict[int, Dict[str, List[str]]]
    active_player_number: int
    is_game_ended: bool

    turns_log: List[Dict[str, str]]
    msgs_log: Dict[str, List[str]]

    MAX_COUNT_OF_SKIPS: int

    def __init__(self,
                 locations: List[Location],
                 items: List[Item],
                 creatures: List[Creature],
                 players: List[Player],
                 adjacence_list: Dict,
                 settings: Dict[str, Any],
                 imagepath: str,
                 seed: Union[int, Any],
                 loadseed: Union[int, Any]) -> None: ...

    # Сообщения.
    def send_msg(self, msg: str, player: Player, priority: int = ...) -> None: ...
    def clear_to_send(self) -> Dict[int, Dict[str, List[str]]]: ...
    def regularize_to_send(self) -> Dict[str, List[str]]: ...
    def player_to_send(self, username: str) -> List[str]: ...
    def get_msgs(self, username: str) -> List[str]: ...

    # Уникальные предметы.
    def set_unique(self, obj: AnyLO, key: str) -> None: ...
    def get_unique(self, key: str) -> AnyLO: ...

    # Ход игрока.
    def make_turn(self, turn: str) -> Dict[str, List[str]]: ...
    def skip_turn(self) -> None: ...
    def get_turns(self, number: Union[int, None] = ..., username: Union[str, None] = ...) -> Union[List[str], str]: ...
    def end_game(self) -> None: ...

    # Активный игрок.
    def get_next_active_player_number(self) -> Union[None, int]: ...
    def get_next_active_player(self) -> Union[None, Player]: ...
    def get_active_player(self) -> Player: ...
    def get_active_player_username(self) -> str: ...
    def get_active_player_ats(self) -> List[str]: ...

    # Объекты Лабиринта.
    def get_all_objects(self) -> Set[AnyLO]: ...
    def get_objects(self,
                    lrtype: Union[str, List[str]] = ...,
                    class_names: Union[str, List[str]] = ...,
                    flags: List[str] = ...,
                    key: Callable[[AnyLO], bool] = lambda x: True): ...

    def save(self) -> str: ...

    def get_buttons(self) -> List[Button]: ...

    def get_bars(self, username: str) -> List[Bar]: ...
