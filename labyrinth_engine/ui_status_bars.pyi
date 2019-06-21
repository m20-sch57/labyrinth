from labyrinth_engine.lr_types import AnyPlayer

from typing import Any, Dict, Union

class Bar:
    def __str__(self) -> str: ...

    def get(self, *args, **kwargs) -> Any: ...


class StringBar(Bar):
    bar_type: str
    name: str
    values: Dict[AnyPlayer, Any]

    def __init__(self, name: str, init_values: Dict[AnyPlayer, Any]) -> None: ...

    def set_value(self, new_value: Any, player: AnyPlayer) -> None: ...

    def set_all_values(self, new_values: Dict[AnyPlayer, Any]) -> None: ...

    def get(self, player: AnyPlayer) -> Dict[str, Union[str, Any]]: ...
