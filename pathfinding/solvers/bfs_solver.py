from collections.abc import Iterable

from ..maze import SolveStep
from .maze_solver import MazeSolver


class BFSSolver(MazeSolver):
    def solve(self) -> Iterable[SolveStep]:
        pass
