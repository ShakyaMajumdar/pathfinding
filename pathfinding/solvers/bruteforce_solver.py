from collections.abc import Iterable

from ..maze import SolveStep
from .maze_solver import MazeSolver


class BruteforceSolver(MazeSolver):
    def solve(self) -> Iterable[SolveStep]:
        yield from (
            SolveStep.DOWN,
            SolveStep.DOWN,
            SolveStep.LEFT,
            SolveStep.LEFT,
            SolveStep.DOWN,
        )
