from collections.abc import Iterable
from typing import Callable

from pathfinding import loaders, renderers, solvers
from pathfinding.maze import Maze, SolveStep


def main(
    loader: Callable[[], loaders.MazeLoader],
    solver: Callable[[Maze], solvers.MazeSolver],
    renderer: Callable[[Maze, Iterable[SolveStep]], renderers.MazeRenderer],
):
    maze = loader().load()
    steps = solver(maze).solve()
    renderer(maze, steps).render()


if __name__ == "__main__":
    main(
        loaders.StandardInputLoader,
        solvers.BruteforceSolver,
        renderers.StandardOutputRenderer,
    )
