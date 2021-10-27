from .maze_renderer_abc import MazeRenderer


class StandardOutputRenderer(MazeRenderer):
    """Renders the maze and the steps to solve it to stdout."""

    def render(self) -> None:
        for _ in self.solver.solve():
            ...
        print(self.solver.get_shortest_path())
