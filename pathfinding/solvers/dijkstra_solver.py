from collections.abc import Iterable, Sequence

from ..maze import Position, SolveStep
from .maze_solver import MazeSolver


class DijkstraSolver(MazeSolver):
    def solve(self) -> Iterable[Position]:
        pass

    def get_shortest_path(self) -> Sequence[SolveStep]:
        pass
