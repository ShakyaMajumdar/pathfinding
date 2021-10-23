import os
import time

from ..maze import CellState, Position
from .maze_renderer import MazeRenderer


class StandardOutputRenderer(MazeRenderer):
    """Renders the maze and the steps to solve it to stdout."""

    def render(self) -> None:
        chars = {CellState.EMPTY: "  ", CellState.WALL: "██"}
        actor_char = "⚪"
        actor_position = Position(*self.maze.entry_point)

        grid_str = [[chars[state] for state in line] for line in self.maze.grid]
        grid_str[self.maze.entry_point.row][self.maze.entry_point.col] = actor_char

        os.system("cls")
        print("\n".join("".join(line) for line in grid_str))
        time.sleep(0.5)

        for step in self.steps:
            grid_str[actor_position.row][actor_position.col] = chars[CellState.EMPTY]
            actor_position = actor_position.apply_step(step)
            grid_str[actor_position.row][actor_position.col] = actor_char

            os.system("cls")
            print("\n".join("".join(line) for line in grid_str))
            time.sleep(0.5)
