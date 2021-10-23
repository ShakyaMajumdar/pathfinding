from abc import ABC, abstractmethod
from collections.abc import Iterable

from ..maze import Maze, SolveStep


class MazeSolver(ABC):
    def __init__(self, maze: Maze):
        self.maze = maze

    @abstractmethod
    def solve(self) -> Iterable[SolveStep]:
        """Return a sequence of steps that will solve the given maze."""
