from labyrinth_engine.lr_types import Player

from typing import Any, Dict, Union, List, Callable

class Bar:
    def __str__(self) -> str: ...

    def get(self, *args, **kwargs) -> Any: ...


class StringBar(Bar):
    def __init__(self, name: str, init_values: Dict[Player, Any]) -> None:
        self.bar_type = ... # type: str
        self.name = ... # type: str
        self.values = ... # type: Dict[Player, Any]

    def set_value(self, new_value: Any, player: Player) -> None: ...

    def set_all_values(self, new_values: Dict[Player, Any]) -> None: ...

    def get(self, player: Player) -> Dict[str, Union[str, Any]]: ...
