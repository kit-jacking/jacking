import math
import geopandas as gpd
from shapely import LineString

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

    def get_path_coordinates(self) -> tuple[list[float], list[float]]:
        if self.previous is None:
            return [self.x], [self.y]
        x, y = self.previous.get_path_coordinates()
        x.append(self.x)
        y.append(self.y)
        return x, y

    def get_path_gpd_geojson(self) -> str:
        x, y = self.get_path_coordinates()
        gdf = gpd.GeoDataFrame(
            geometry=gpd.points_from_xy(x, y),
            crs="EPSG:2180"
        )
        return gdf.to_json(to_wgs84=True)

    def get_path_gdf(self):
        x, y = self.get_path_coordinates()
        line: LineString = LineString(list(zip(x, y)))

        gdf = gpd.GeoDataFrame(
            geometry=[line],
            crs="EPSG:2180"
        )

        return gdf

    def save_path_geopandas_shp(self, filename_to_be_saved: str) -> None:
        self.get_path_gdf().to_file(filename_to_be_saved + ".shp")

    def save_path_geopandas_geojson(self, filename_to_be_saved: str):
        self.get_path_gdf().to_file(filename_to_be_saved + ".geojson", driver='GeoJSON')