from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence

from ..maze import Maze, Position, SolveStep


class MazeSolver(ABC):
    def __init__(self, maze: Maze):
        self.maze = maze
        self.shortest_distances: list[list[float]] = [[float("inf")] * len(row) for row in maze.grid]
        self._completed = False

    @abstractmethod
    def solve(self) -> Iterable[Position]:
        """
        Returns an iterable of positions as they are explored by the solver.

        Sets the `shortest_distances` attribute to a 2D list representing the shortest distance of the corresponding
        cell in the maze from the entry point.
        """

    @abstractmethod
    def get_shortest_path(self) -> Sequence[SolveStep]:
        """
        Returns the sequence of `SolveStep`s representing the shortest path from the entry point to the exit point.
        """
