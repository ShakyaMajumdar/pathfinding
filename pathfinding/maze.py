from collections import deque
from collections.abc import Iterator
from enum import Enum, auto
from typing import Callable, Generic, NamedTuple, TypeVar

from .graph import Edge, Graph, Vertex


class CellState(Enum):
    EMPTY = auto()
    WALL = auto()


class SolveStep(tuple[int, int], Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __invert__(self) -> "SolveStep":
        return {
            SolveStep.UP: SolveStep.DOWN,
            SolveStep.DOWN: SolveStep.UP,
            SolveStep.LEFT: SolveStep.RIGHT,
            SolveStep.RIGHT: SolveStep.LEFT,
        }[self]


class Position(NamedTuple):
    row: int
    col: int

    def apply_step(self, step: SolveStep) -> "Position":
        delta_row, delta_col = step
        return Position(self.row + delta_row, self.col + delta_col)

    def __repr__(self) -> str:
        return f"({self.row}, {self.col})"


T = TypeVar("T")


class Grid(Generic[T]):
    """
    Represents a 2D structure which can be indexed by instances of Position and two-tuples.
    Does not allow negative indexing.
    """

    def __init__(self, elements: list[list[T]]):
        self._elements = elements

    def __getitem__(self, item: tuple[int, int]) -> T:
        row, col = item
        if row < 0 or col < 0:
            raise IndexError("list index out of range")
        return self._elements[row][col]

    def __setitem__(self, key: tuple[int, int], value: T) -> None:
        row, col = key
        self._elements[row][col] = value

    def __iter__(self) -> Iterator[tuple[Position, T]]:
        for row, row_elements in enumerate(self._elements):
            for col, element in enumerate(row_elements):
                yield Position(row, col), element

    def on_boundary(self, position: tuple[int, int]) -> bool:
        """Return whether the given position lies on the boundary of the grid."""
        n_rows, n_cols = self.dimensions
        row, col = position
        return row in (0, n_rows - 1) or col in (0, n_cols - 1)

    def get_neighbours_where_predicate(
        self, position: tuple[int, int], predicate: Callable[[tuple[Position, T]], bool] = lambda _: True
    ) -> list[tuple[SolveStep, T]]:
        neighbours: list[tuple[SolveStep, T]] = []
        position = Position(*position)
        for step in SolveStep:
            try:
                neighbour_position = position.apply_step(step)
                if predicate((neighbour_position, self[neighbour_position])):
                    neighbours.append((step, self[neighbour_position]))
            except IndexError:
                pass
        return neighbours

    def __repr__(self) -> str:
        return repr(self._elements)

    @classmethod
    def from_dimensions(cls, dims: tuple[int, int], default: T) -> "Grid[T]":
        """Initialise a grid with the given dimensions and default value."""
        rows, cols = dims
        return cls([[default for _ in range(cols)] for _ in range(rows)])

    @classmethod
    def from_dimensions_with_factory(
        cls, dims: tuple[int, int], default_factory: Callable[[tuple[int, int]], T]
    ) -> "Grid[T]":
        """Initialise a grid with the given dimensions and default value."""
        rows, cols = dims
        return cls([[default_factory((row, col)) for col in range(cols)] for row in range(rows)])

    @property
    def dimensions(self) -> tuple[int, int]:
        return len(self._elements), len(self._elements[0])


MazeVertex = Vertex[Position, list[SolveStep]]
MazeEdge = Edge[Position, list[SolveStep]]
MazeGraph = Graph[Position, list[SolveStep]]


class Maze:
    def __init__(self, grid: Grid[CellState], entry_point: Position, exit_point: Position):
        self.grid = grid
        self.entry_point = entry_point
        self.exit_point = exit_point

        if not self.grid[entry_point] == self.grid[exit_point] == CellState.EMPTY:
            raise ValueError("entry point and exit point are not empty")

    def to_graph(self) -> MazeGraph:
        """Convert the maze to a graph."""
        graph = MazeGraph()
        visited_positions = set[Position]()
        visited_position_pairs = set[tuple[Position, Position]]()

        vertex_grid: Grid[MazeVertex] = Grid.from_dimensions_with_factory(
            self.grid.dimensions, lambda pos: MazeVertex(Position(*pos))
        )

        for root_position, root_vertex in vertex_grid:
            if root_position in visited_positions or self.grid[root_position] != CellState.EMPTY:
                continue

            exploration_queue: deque[tuple[MazeVertex, MazeEdge]] = deque()

            visited_positions.add(root_position)
            for other_neighbour_direction, other_neighbour_vertex in vertex_grid.get_neighbours_where_predicate(
                root_position, lambda tup: self.grid[tup[0]] == CellState.EMPTY
            ):
                new_edge = MazeEdge([other_neighbour_direction], tail=root_vertex, head=other_neighbour_vertex)
                root_vertex.edges.add(new_edge)
                other_neighbour_vertex.edges.add(new_edge)
                graph.add_edge(new_edge)
                visited_position_pairs.add((root_position, other_neighbour_vertex.data))
                exploration_queue.append((other_neighbour_vertex, new_edge))

            while exploration_queue:
                vertex, edge = exploration_queue.popleft()
                parent_neighbour_position = vertex.data.apply_step(~edge.data[-1])

                if (vertex.data, parent_neighbour_position) in visited_position_pairs:
                    graph.remove_edge(edge)
                    continue
                visited_position_pairs.add((parent_neighbour_position, vertex.data))

                if vertex.data in visited_positions:
                    continue
                visited_positions.add(vertex.data)

                other_neighbours: list[tuple[SolveStep, MazeVertex]] = vertex_grid.get_neighbours_where_predicate(
                    vertex.data,
                    lambda tup: self.grid[tup[0]] == CellState.EMPTY and tup[1].data != parent_neighbour_position,
                )

                if len(other_neighbours) == 0:
                    continue

                if len(other_neighbours) == 1:
                    other_neighbour_direction, other_neighbour_vertex = other_neighbours[0]
                    graph.remove_vertex(vertex)
                    vertex.edges.remove(edge)
                    other_neighbour_vertex.edges.add(edge)
                    edge.head = other_neighbour_vertex
                    edge.data.append(other_neighbour_direction)
                    exploration_queue.append((other_neighbour_vertex, edge))
                    continue

                for other_neighbour_direction, other_neighbour_vertex in other_neighbours:
                    new_edge = MazeEdge([other_neighbour_direction], tail=vertex, head=other_neighbour_vertex)
                    other_neighbour_vertex.edges.add(new_edge)
                    graph.add_edge(new_edge)
                    exploration_queue.append((other_neighbour_vertex, new_edge))

        return graph
