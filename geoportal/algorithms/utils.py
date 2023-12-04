import geopandas as gpd
from shapely import LineString
import math


def get_linestring_geometry(row: gpd.GeoSeries) -> LineString:
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


def get_distance_between_nodes(node_one: "Node", node_two: "Node") -> float:
    return math.sqrt((node_one.x - node_two.y) ** 2 + (node_one.y - node_two.y) ** 2)
