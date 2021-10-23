from enum import Enum, auto
from typing import NamedTuple


class CellState(Enum):
    EMPTY = auto()
    WALL = auto()


class SolveStep(tuple[int, int], Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Position(NamedTuple):
    row: int
    col: int

    def apply_step(self, step: SolveStep) -> "Position":
        delta_row, delta_col = step
        return Position(self.row + delta_row, self.col + delta_col)


class Maze:
    def __init__(self, grid: list[list[CellState]], entry_point: Position, exit_point: Position):
        self.grid = grid
        self.entry_point = entry_point
        self.exit_point = exit_point
        if not self[entry_point] == self[exit_point] == CellState.EMPTY:
            raise ValueError("entry point and exit point are not empty")

    def __getitem__(self, position: Position) -> CellState:
        return self.grid[position.row][position.col]
