from abc import ABC, abstractmethod

from ..maze import Maze
from ..solvers import MazeSolver


class MazeRenderer(ABC):
    def __init__(self, maze: Maze, solver: MazeSolver):
        self.maze = maze
        self.solver = solver

    @abstractmethod
    def render(self) -> None:
        """Render the application of the steps on the maze"""
