from enum import Enum, auto
from typing import TypeAlias


class CellState(Enum):
    EMPTY = auto()
    WALL = auto()


Maze: TypeAlias = list[list[CellState]]
Position: TypeAlias = tuple[int, int]
