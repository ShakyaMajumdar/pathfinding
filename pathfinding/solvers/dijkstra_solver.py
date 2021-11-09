from collections import defaultdict
from collections.abc import Iterable, Sequence

from ..data_structures import Heap, Position, PriorityQueue, SolveStep
from ..maze import MazeVertex
from .maze_solver_abc import MazeSolver


class DijkstraSolver(MazeSolver):
    def solve(self) -> Iterable[Position]:
        graph = self.maze.to_graph()
        source = next(vertex for vertex in graph.vertices if vertex.data == self.maze.entry_point)
        visited: set[MazeVertex] = {source}
        self.shortest_distances: defaultdict[MazeVertex, float] = defaultdict(lambda: float("inf"))
        self.shortest_distances[source] = 0
        priority_queue: PriorityQueue[MazeVertex] = Heap()

        for vertex in graph.vertices:
            priority_queue.push(vertex, self.shortest_distances[vertex])

        while priority_queue:
            vertex = priority_queue.pop()
            visited.add(vertex)
            for edge in vertex.edges:

                other_end = edge.get_other_end(vertex)

                if other_end in visited:
                    continue
                new_dist = min(self.shortest_distances[other_end], self.shortest_distances[vertex] + len(edge.data))
                self.shortest_distances[other_end] = new_dist
                priority_queue.decrease_priority(other_end, new_dist)

            yield vertex.data

        self._completed = True

    def get_shortest_path(self) -> Sequence[SolveStep]:
        if not self._completed:
            raise RuntimeError("solve method was not called")

        return []
