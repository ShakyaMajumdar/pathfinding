import operator
from collections import deque
from collections.abc import Iterable, Sequence

from ..maze import CellState, Position, SolveStep
from .maze_solver_abc import MazeSolver


class BFSSolver(MazeSolver):
    def solve(self) -> Iterable[Position]:
        self.shortest_distances[self.maze.entry_point] = 0

        exploration_queue: deque[Position] = deque([self.maze.entry_point])
        visited: set[Position] = set()

        while exploration_queue:
            position = exploration_queue.popleft()
            visited.add(position)

            for direction, neighbour in self.maze.grid.get_neighbours_where_predicate(position):
                neighbour_position = position.apply_step(direction)
                if neighbour == CellState.WALL or neighbour_position in visited:
                    continue
                self.shortest_distances[neighbour_position] = 1 + self.shortest_distances[position]
                exploration_queue.append(neighbour_position)

            yield position
        self._completed = True

    def get_shortest_path(self) -> Sequence[SolveStep]:
        if not self._completed:
            raise RuntimeError("solve method was not called")

        steps: deque[SolveStep] = deque([])

        current = self.maze.exit_point
        while current != self.maze.entry_point:
            next_step, _ = min(
                self.shortest_distances.get_neighbours_where_predicate(current), key=operator.itemgetter(1)
            )
            steps.appendleft(~next_step)
            current = current.apply_step(next_step)

        return steps
