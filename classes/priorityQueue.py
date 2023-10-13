import heapq
from classes.node import Node


class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, Node]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, node: Node, priority: float):
        heapq.heappush(self.elements, (priority, node))

    def get(self) -> Node:
        return heapq.heappop(self.elements)[1]
