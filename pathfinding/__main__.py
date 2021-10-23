from typing import Type

from pathfinding import loaders, renderers, solvers


def main(
    loader: Type[loaders.MazeLoader],
    solver: Type[solvers.MazeSolver],
    renderer: Type[renderers.MazeRenderer],
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
