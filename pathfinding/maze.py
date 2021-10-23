from enum import Enum, auto
from typing import TypeAlias


class CellState(Enum):
    EMPTY = auto()
    WALL = auto()


class SolveStep(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


Position: TypeAlias = tuple[int, int]


class Maze:
    def __init__(self, maze: list[list[CellState]], entry_point: Position, exit_point: Position):
        self._maze = maze
        self.entry_point = entry_point
        self.exit_point = exit_point
        if not self[entry_point] == self[exit_point] == CellState.EMPTY:
            raise ValueError("entry point and exit point are not empty")

    def __getitem__(self, item: Position) -> CellState:
        row, col = item
        return self._maze[row][col]
