from abc import ABC, abstractmethod
from collections.abc import Sequence
from enum import Enum, auto

from ..maze import Maze, Position


class SolveStep(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class MazeSolver(ABC):
    @abstractmethod
    def solve(
        self, maze: Maze, entry_point: Position, exit_point: Position
    ) -> Sequence[SolveStep]:
        """Return a sequence of steps that will solve the given maze."""
