from textwrap import dedent
from typing import Optional

from ..maze import CellState, Maze, Position
from .maze_loader import MazeLoader


def on_boundary(dims: tuple[int, int], position: tuple[int, int]) -> bool:
    n_rows, n_cols = dims
    row, col = position
    return row in (0, n_rows - 1) or col in (0, n_cols - 1)


def parse_maze(maze_str: list[str]) -> Maze:
    """
    Parse a maze from a string representation.
    # -> wall
    . -> empty
    X -> entry point
    Y -> exit point
    :param maze_str: A list of strings representing the rows of a maze.
    :return: A maze.
    :raises:
        IndexError: If the maze is empty
        ValueError: If all rows are not of the same length
        ValueError: If the entry point or exit point are not on the boundary
        ValueError: If an attempt is made to set the entry point or exit point more than once
        ValueError: If the entry point or exit point are not set
        ValueError: If an unrecognized character is present
    """
    n_rows = len(maze_str)
    if n_rows == 0:
        raise IndexError("empty maze")

    n_cols = len(maze_str[0])
    if not all(len(line) == n_cols for line in maze_str):
        raise ValueError("all rows are not of the same size")

    maze: list[list[CellState]] = []
    entry_position: Optional[Position] = None
    exit_position: Optional[Position] = None

    for row, line in enumerate(maze_str):
        parsed_line: list[CellState] = []
        for col, char in enumerate(line):
            if char == "#":
                parsed_line.append(CellState.WALL)

            elif char == ".":
                parsed_line.append(CellState.EMPTY)

            elif char == "X":
                if not on_boundary((n_rows, n_cols), (row, col)):
                    raise ValueError(f"entry point at row: {row}, col: {col} is not on boundary of maze")
                if entry_position is not None:
                    raise ValueError(
                        f"entry point already set at row: {entry_position.row}, col: {entry_position.col}, "
                        f"attempted to set again at row: {row}, col: {col}"
                    )
                parsed_line.append(CellState.EMPTY)
                entry_position = Position(row, col)

            elif char == "Y":
                if not on_boundary((n_rows, n_cols), (row, col)):
                    raise ValueError(f"exit point at row: {row}, col: {col} is not on boundary of maze")
                if exit_position is not None:
                    raise ValueError(
                        f"entry point already set at row: {exit_position.row}, col: {exit_position.col}, "
                        f"attempted to set again at row: {row}, col: {col}"
                    )
                parsed_line.append(CellState.EMPTY)
                exit_position = Position(row, col)

            else:
                raise ValueError(f"unrecognized character {char} at row: {row}, col: {col}")

        maze.append(parsed_line)

    if entry_position is None:
        raise ValueError("entry position not set")

    if exit_position is None:
        raise ValueError("exit position not set")

    return Maze(maze, entry_position, exit_position)


class StandardInputLoader(MazeLoader):
    """Loads a maze by reading from stdin."""

    def load(self) -> Maze:
        print(
            dedent(
                """
                Enter your maze. Use # for walls, . for empty spaces, X for the entry point and Y for the exit point.
                Enter a blank line when you're done.
                """
            )
        )

        maze = []
        while line := input():
            maze.append(line)

        return parse_maze(maze)
