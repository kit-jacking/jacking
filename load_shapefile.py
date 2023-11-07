import geopandas as gpd
from shapely import LineString

from classes.conjunctionManager import ConjunctionManager
from classes.edge import Edge
from classes.graph import Graph
from classes.node import Node


def create_node_name_from_coords(coords: tuple[float, float]) -> str:
    return f"Node {coords[0]}x{coords[1]}"


def create_nodes_from_linestring(linestring: LineString) -> tuple[Node, Node]:
    start_coords = linestring.coords[0]
    node_start = Node(create_node_name_from_coords(start_coords),
                      start_coords[0],
                      start_coords[1])
    end_coords = linestring.coords[-1]
    node_end = Node(create_node_name_from_coords(end_coords),
                    end_coords[0],
                    end_coords[1])
    return node_start, node_end


def create_edge_from_linestring(linestring: LineString,
                                node_start: Node,
                                node_end: Node,
                                edge_id: str) -> Edge:
    return Edge(node_start, node_end, linestring.length, edge_id)


def load_shapefile(file_to_load: str) -> Graph:
    df = gpd.read_file(file_to_load)

    nodes: list[Node] = []
    edges: list[Edge] = []
    conjunction_manager = ConjunctionManager()

    for i, row in df.iterrows():
        linestring = row.geometry.geom_type.startswith("LineString")
        if not linestring:
            print("Not linestring: ", row.geometry.geom_type)
            continue

        geom: LineString = row.geometry

        probable_node_start, probable_node_end = create_nodes_from_linestring(geom)

        node_start = conjunction_manager.get_conjunction(probable_node_start)
        node_end = conjunction_manager.get_conjunction(probable_node_end)
        nodes.append(node_start)
        nodes.append(node_end)

        edge = create_edge_from_linestring(geom, node_start, node_end, row["LOKALNYID"])
        edge2 = create_edge_from_linestring(geom, node_end, node_start, row["LOKALNYID"])

        edges.append(edge)
        edges.append(edge2)

    graph = Graph(list(nodes), list(edges))
    return graph


if __name__ == "__main__":
    filename = "shapefiles/Halinow Highways Latane/Halinow Highways Latane.shp"
    load_shapefile(filename)
