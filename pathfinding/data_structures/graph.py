from dataclasses import dataclass, field
from typing import ClassVar, Generic, TypeVar

V = TypeVar("V")
E = TypeVar("E")


@dataclass
class Vertex(Generic[V, E]):
    data: V
    edges: set["Edge[V, E]"] = field(default_factory=set)
    _counter: ClassVar[int] = 0

    def __post_init__(self) -> None:
        self._id = Vertex._counter
        Vertex._counter += 1

    def __hash__(self) -> int:
        return hash(self._id)


@dataclass
class Edge(Generic[V, E]):
    data: E
    tail: Vertex[V, E]
    head: Vertex[V, E]
    _counter: ClassVar[int] = 0

    def get_other_end(self, vertex: Vertex[V, E]) -> Vertex[V, E]:
        return self.head if vertex == self.tail else self.tail

    def __post_init__(self) -> None:
        self._id = Edge._counter
        Edge._counter += 1

    def __hash__(self) -> int:
        return hash(self._id)


@dataclass
class Graph(Generic[V, E]):
    vertices: set[Vertex[V, E]] = field(default_factory=set)
    edges: set[Edge[V, E]] = field(default_factory=set)

    def add_edge(self, edge: Edge[V, E]) -> None:
        self.edges.add(edge)
        self.vertices.update({edge.head, edge.tail})

    def remove_edge(self, edge: Edge[V, E]) -> None:
        self.edges.remove(edge)

    def add_vertex(self, vertex: Vertex[V, E]) -> None:
        self.vertices.add(vertex)
        self.edges.update(vertex.edges)

    def remove_vertex(self, vertex: Vertex[V, E]) -> None:
        self.vertices.remove(vertex)
