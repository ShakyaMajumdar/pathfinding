from enum import Enum, auto
from typing import Generic, NamedTuple, TypeVar


class CellState(Enum):
    EMPTY = auto()
    WALL = auto()


class SolveStep(tuple[int, int], Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __invert__(self) -> "SolveStep":
        return {
            SolveStep.UP: SolveStep.DOWN,
            SolveStep.DOWN: SolveStep.UP,
            SolveStep.LEFT: SolveStep.RIGHT,
            SolveStep.RIGHT: SolveStep.LEFT,
        }[self]


class Position(NamedTuple):
    row: int
    col: int

    def apply_step(self, step: SolveStep) -> "Position":
        delta_row, delta_col = step
        return Position(self.row + delta_row, self.col + delta_col)


T = TypeVar("T")


class Grid(Generic[T]):
    """Represents a 2D structure which can be indexed by instances of Position and two-tuples."""

    def __init__(self, elements: list[list[T]]):
        self._elements = elements

    def __getitem__(self, item: tuple[int, int]) -> T:
        row, col = item
        return self._elements[row][col]

    def __setitem__(self, key: tuple[int, int], value: T) -> None:
        row, col = key
        self._elements[row][col] = value

    def on_boundary(self, position: tuple[int, int]) -> bool:
        """Return whether the given position lies on the boundary of the grid."""
        n_rows, n_cols = self.dimensions
        row, col = position
        return row in (0, n_rows - 1) or col in (0, n_cols - 1)

    def get_neighbours(self, position: tuple[int, int]) -> list[tuple[SolveStep, T]]:
        neighbours: list[tuple[SolveStep, T]] = []
        position = Position(*position)
        for step in SolveStep:
            try:
                neighbour_position = position.apply_step(step)
                neighbours.append((step, self[neighbour_position]))
            except IndexError:
                pass
        return neighbours

    def __repr__(self) -> str:
        return repr(self._elements)

    @classmethod
    def from_dimensions(cls, dims: tuple[int, int], default: T) -> "Grid[T]":
        """Initialise a grid with the given dimensions and default value."""
        rows, cols = dims
        return cls([[default for _ in range(cols)] for _ in range(rows)])

    @property
    def dimensions(self) -> tuple[int, int]:
        return len(self._elements), len(self._elements[0])


class Maze:
    def __init__(self, grid: Grid[CellState], entry_point: Position, exit_point: Position):
        self.grid = grid
        self.entry_point = entry_point
        self.exit_point = exit_point

        if not self.grid[entry_point] == self.grid[exit_point] == CellState.EMPTY:
            raise ValueError("entry point and exit point are not empty")
