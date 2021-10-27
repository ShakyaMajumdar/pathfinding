from abc import ABC, abstractmethod

from ..maze import Maze


class MazeLoader(ABC):
    @abstractmethod
    def load(self) -> Maze:
        """Load and return a maze."""
