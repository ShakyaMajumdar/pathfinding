from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from math import ceil
from typing import Generic, TypeVar

T = TypeVar("T")


class PriorityQueue(Generic[T], ABC):
    @abstractmethod
    def __init__(self, *elements_with_priorities: tuple[T, float]):
        """Initialize a priority queue with the given elements and priorities."""

    @abstractmethod
    def push(self, element: T, priority: float) -> None:
        """Add the given element with the given priority to the priority queue."""

    @abstractmethod
    def pop(self) -> T:
        """Remove and return the element with the minimum priority."""

    @abstractmethod
    def peek(self) -> T:
        """Return the element with the minimum priority without removing it."""

    @abstractmethod
    def decrease_priority(self, element: T, new_priority: float) -> None:
        """Update the priority of the given element to the new priority."""

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of elements currently in the priority queue."""


@dataclass(order=True)
class _HeapEntry(Generic[T]):
    priority: float
    index: int
    element: T = field(compare=False)


class Heap(PriorityQueue[T]):
    def __init__(self, *elements_with_priorities: tuple[T, float]):
        self._heap: list[_HeapEntry[T]] = []
        self._element_index_map: dict[T, int] = {}

        for element, priority in elements_with_priorities:
            self.push(element, priority)

    def push(self, element: T, priority: float) -> None:
        self._heap.append(_HeapEntry(priority, len(self._heap), element))
        self._element_index_map[element] = len(self._heap) - 1
        self.sift_up(len(self._heap) - 1)

    def pop(self) -> T:
        popped = self.peek()
        self._element_index_map.pop(popped)
        last_element = self._heap.pop()
        if self._heap:
            self._heap[0] = last_element
            self._element_index_map[self._heap[0].element] = 0
            self.sift_down()
        return popped

    def peek(self) -> T:
        return self._heap[0].element

    def decrease_priority(self, element: T, new_priority: float) -> None:
        index = self._element_index_map[element]
        if self._heap[index].priority < new_priority:
            raise ValueError("New priority is greater than current priority.")
        self._heap[index].priority = new_priority
        self.sift_up(index)

    def __len__(self) -> int:
        return len(self._heap)

    def sift_up(self, index: int) -> None:
        parent_index = ceil(index / 2) - 1
        while index > 0 and self._heap[index] < self._heap[parent_index]:
            self._swap_indices(index, parent_index)
            index = parent_index
            parent_index = ceil(parent_index / 2) - 1

    def sift_down(self) -> None:
        index = 0
        if 2 * index + 2 >= len(self._heap):
            return
        min_child_index = min((2 * index + 1, 2 * index + 2), key=lambda i: self._heap[i])
        while index < len(self._heap) and self._heap[index] > self._heap[min_child_index]:
            self._swap_indices(index, min_child_index)
            index = min_child_index
            if 2 * index + 2 >= len(self._heap):
                return
            min_child_index = min((2 * index + 1, 2 * index + 2), key=lambda i: self._heap[i])

    def _swap_indices(self, i1: int, i2: int) -> None:
        self._heap[i1], self._heap[i2] = self._heap[i2], self._heap[i1]
        self._element_index_map.update({self._heap[i1].element: i1, self._heap[i2].element: i2})

    def __repr__(self) -> str:
        entries = ", ".join(f"(element={entry.element}, priority={entry.priority})" for entry in self._heap)
        return f"Heap({entries})"
