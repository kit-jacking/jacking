from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.node import Node


class Edge:
    def __init__(self, start: "Node", end: "Node", cost: float, id: str | None = None):
        if start is None or end is None or cost < 0:
            raise RuntimeError("Edge initialization failed. Wrong arguments.")
        self.start: "Node" = start
        self.end: "Node" = end
        self.cost: float = cost
        self.id = id

    def __str__(self):
        return f"{self.start.name} -> {self.end.name}"
