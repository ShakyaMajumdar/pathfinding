from .maze_renderer import MazeRenderer


class StandardOutputRenderer(MazeRenderer):
    def render(self):
        print("\n".join(" ".join(str(state) for state in line) for line in self.maze.grid))
