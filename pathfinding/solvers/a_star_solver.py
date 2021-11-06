from collections.abc import Iterable, Sequence

from ..data_structures import Position, SolveStep
from .maze_solver_abc import MazeSolver


class AStarSolver(MazeSolver):
    def solve(self) -> Iterable[Position]:
        pass

    def get_shortest_path(self) -> Sequence[SolveStep]:
        pass
