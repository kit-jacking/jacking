import math

import geopandas as gpd
from shapely import LineString, Point, MultiLineString
from shapely.ops import linemerge

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

    def get_linestring_geometry(self, row: gpd.GeoSeries) -> LineString:
        geom_type: str = row.geometry.geom_type
        if geom_type.startswith("LineString"):
            geom: LineString = row.geometry
        elif geom_type.startswith("MultiLineString"):
            if len(row.geometry.geoms) > 1:
                raise RuntimeError(
                    "Multilinestring has more than 1 linestrings which is not allowed. Fix input data. It currently has: " +
                    len(row.geometry.geoms))
            geom: LineString = row.geometry.geoms[0]
        else:
            raise RuntimeError("Last geometry was not linestring nor multilinestring: " + row.geometry.geom_type)
        return geom

    def get_path_gdf(self, original_gdf: gpd.GeoDataFrame, get_linestrings: bool = False) -> gpd.GeoDataFrame:
        ids = self.get_path_edges_ids()
        if get_linestrings or len(original_gdf.iloc[ids]) == 1:
            gdf = original_gdf.iloc[ids]
            return gdf

        if len(original_gdf.iloc[ids]) == 0:
            raise RuntimeError("There are no linestrings on the path")

        line_strings: list[LineString] = []
        for i, row in original_gdf.iloc[ids].iterrows():
            geom: LineString = self.get_linestring_geometry(row)
            line_strings.append(geom)
            continue

        path: LineString = linemerge(MultiLineString(line_strings))
        path_points = [Point(x) for x in path.coords]
        path_points = path_points[::-1]
        gdf = gpd.GeoDataFrame(geometry=path_points)
        gdf['id'] = range(0, len(gdf))
        return gdf

    def get_path_length(self, original_gdf: gpd.GeoDataFrame, length_crs: str = "EPSG:2180") -> float:
        ids = self.get_path_edges_ids()
        gdf = original_gdf.iloc[ids]
        gdf = gdf.to_crs(length_crs)
        return sum(gdf.geometry.length)