from collections.abc import Callable, Iterator
from enum import Enum
from typing import Generic, NamedTuple, TypeVar

T = TypeVar("T")


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

    def __repr__(self) -> str:
        return f"({self.row}, {self.col})"


class Grid(Generic[T]):
    """
    Represents a 2D structure which can be indexed by instances of Position and two-tuples.
    Does not allow negative indexing.
    """

    def __init__(self, elements: list[list[T]]):
        self._elements = elements

    def __getitem__(self, item: tuple[int, int]) -> T:
        row, col = item
        if row < 0 or col < 0:
            raise IndexError("list index out of range")
        return self._elements[row][col]

    def __setitem__(self, key: tuple[int, int], value: T) -> None:
        row, col = key
        self._elements[row][col] = value

    def __iter__(self) -> Iterator[tuple[Position, T]]:
        for row, row_elements in enumerate(self._elements):
            for col, element in enumerate(row_elements):
                yield Position(row, col), element

    def on_boundary(self, position: tuple[int, int]) -> bool:
        """Return whether the given position lies on the boundary of the grid."""
        n_rows, n_cols = self.dimensions
        row, col = position
        return row in (0, n_rows - 1) or col in (0, n_cols - 1)

    def get_neighbours_where_predicate(
        self, position: tuple[int, int], predicate: Callable[[tuple[Position, T]], bool] = lambda _: True
    ) -> list[tuple[SolveStep, T]]:
        neighbours: list[tuple[SolveStep, T]] = []
        position = Position(*position)
        for step in SolveStep:
            try:
                neighbour_position = position.apply_step(step)
                if predicate((neighbour_position, self[neighbour_position])):
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

    @classmethod
    def from_dimensions_with_factory(
        cls, dims: tuple[int, int], default_factory: Callable[[tuple[int, int]], T]
    ) -> "Grid[T]":
        """Initialise a grid with the given dimensions and default value."""
        rows, cols = dims
        return cls([[default_factory((row, col)) for col in range(cols)] for row in range(rows)])

    @property
    def dimensions(self) -> tuple[int, int]:
        return len(self._elements), len(self._elements[0])
