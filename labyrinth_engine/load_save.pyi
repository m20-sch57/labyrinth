from labyrinth_engine.labyrinth import Labyrinth
from typing import Any, Dict, Union, List


def load_save(save: Union[str, Dict[str, Union[int, List[str], List[Dict[str, str]]]]], _map: Union[str, Dict]) -> Labyrinth: ...


def load_map(_map: Union[str, Dict], users: List[str], loadseed: Union[int, Any] = ..., **kwargs) -> Labyrinth: ...
