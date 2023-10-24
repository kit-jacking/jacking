from classes.node import Node
from classes.edge import Edge


class Graph:
    def __init__(self, nodes: list[Node], edges: list[Edge]):
        self.nodes: list[Node] = nodes
        self.edges: list[Edge] = edges
        for edge in self.edges:
            edge.start.add_neighbour(edge)
