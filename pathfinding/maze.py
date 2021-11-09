from collections import deque
from enum import Enum, auto

from .data_structures.graph import Edge, Graph, Vertex
from .data_structures.grid import Grid, Position, SolveStep


class CellState(Enum):
    EMPTY = auto()
    WALL = auto()


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
                    edge.tail.edges.remove(edge)
                    edge.head.edges.remove(edge)
                    if not edge.tail.edges:
                        graph.remove_vertex(edge.tail)
                    if not edge.head.edges:
                        graph.remove_vertex(edge.head)
                    print("edge rem", edge.tail.data, edge.head.data)
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
                    vertex.edges.add(new_edge)
                    graph.add_edge(new_edge)
                    exploration_queue.append((other_neighbour_vertex, new_edge))

        return graph
