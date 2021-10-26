from typing import Callable

from pathfinding import loaders, renderers, solvers
from pathfinding.maze import Maze


def main(
    loader_factory: Callable[[], loaders.MazeLoader],
    solver_factory: Callable[[Maze], solvers.MazeSolver],
    renderer_factory: Callable[[Maze, solvers.MazeSolver], renderers.MazeRenderer],
) -> None:
    loader = loader_factory()
    maze = loader.load()

    solver = solver_factory(maze)

    renderer = renderer_factory(maze, solver)
    renderer.render()


if __name__ == "__main__":
    main(
        loaders.StandardInputLoader,
        solvers.BFSSolver,
        renderers.StandardOutputRenderer,
    )
