import math

import geopandas as gpd

from classes.edge import Edge


class Node:
    def __init__(self, name: str, x: float, y: float, neighbours: list[Edge] = None,
                 g: float = math.inf, f: float = math.inf, previous: "Node" = None):
        # Name should be unique
        self.name: str = name
        self.x: float = x
        self.y: float = y

        if neighbours:
            self.neighbours: list[Edge] = neighbours
        else:
            self.neighbours: list[Edge] = []

        self.g: float = g
        self.f: float = f
        self.previous: tuple["Node", Edge] | None = previous

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

        return f"{self.name} -> " + self.previous[0].path()

    def __str__(self):
        return f"{self.name}({self.x}, {self.y}), neighbours: {[f'{edge.end.name} length: {edge.length}' for edge in self.neighbours]}"

    def __lt__(self, node: "Node"):
        if type(node) is not type(self):
            raise RuntimeError

        return self.f < node.f

    def copy(self):
        return Node(self.name, self.x, self.y, self.neighbours, self.g, self.f, self.previous)

    def get_path_edges_ids(self) -> list[int]:
        if self.previous is None:
            return []
        path = self.previous[0].get_path_edges_ids()
        path.append(self.previous[1].id)
        return path

    def get_path_gdf(self, original_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        ids = self.get_path_edges_ids()
        gdf = original_gdf.iloc[ids]

        return gdf