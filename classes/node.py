import math
from classes.edge import Edge


class Node:
    def __init__(self, name: str, x: float, y: float, neighbours: list[Edge] = None,
                 g: float = math.inf, f: float = math.inf, previous: "Node" = None):
        self.name: str = name
        self.x: float = x
        self.y: float = y

        if neighbours:
            self.neighbours: list[Edge] = neighbours
        else:
            self.neighbours: list[Edge] = []

        self.g: float = g
        self.f: float = f
        self.previous: "Node" = previous

    def add_neighbour(self, edge: Edge):
        if edge.start is not self:
            raise RuntimeError("edge.start is not self!")
        if edge not in self.neighbours:
            self.neighbours.append(edge)

    def add_neighbours(self, nodes_and_costs: list[Edge]) -> None:
        if not nodes_and_costs:
            return
        for edge in nodes_and_costs:
            self.add_neighbour(edge)

    def path(self):
        if self.previous is None:
            return self.name

        return f"{self.name} -> " + self.previous.path()

    def __str__(self):
        return f"{self.name}({self.x}, {self.y}), neighbours: {[f'{edge.end.name} cost: {edge.cost}' for edge in self.neighbours]}"

    def __lt__(self, node: "Node"):
        if type(node) is not type(self):
            raise RuntimeError

        return self.f < node.f

    def copy(self):
        return Node(self.name, self.x, self.y, self.neighbours, self.g, self.f, self.previous)

    def edge_geo(self):
        if self.previous is None:
            return '[' + str(self.x) + ', ' + str(self.y) + '] '

        return '[' + str(self.x) + ', ' + str(self.y) + '], ' + self.previous.edge_geo()

    def create_geojson(self):
        rtrn = '{"type": "FeatureCollection","features": [{"type": "Feature","properties": {"name": "EPSG:2180"}, "geometry": {"coordinates": ['
        rtrn += self.edge_geo()
        rtrn += '], "type": "LineString"}}]}'
        return rtrn

