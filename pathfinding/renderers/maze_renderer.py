from abc import ABC, abstractmethod
from collections.abc import Iterable

from ..maze import Maze, SolveStep


class MazeRenderer(ABC):
    def __init__(self, maze: Maze, steps: Iterable[SolveStep]):
        self.maze = maze
        self.steps = steps

    @abstractmethod
    def render(self) -> None:
        """Render the application of the steps on the maze"""
