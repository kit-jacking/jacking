import geopandas as gpd
from shapely import LineString

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
                                node_end: Node) -> Edge:
    return Edge(node_start, node_end, linestring.length)


def load_shapefile(file_to_load: str) -> Graph:
    df = gpd.read_file(file_to_load)

    nodes_names: list[str] = []
    nodes: list[Node] = []
    edges: list[Edge] = []

    for i, row in df.iterrows():
        linestring = row.geometry.geom_type.startswith("LineString")
        if not linestring:
            print("Not linestring: ", row.geometry.geom_type)
            continue

        geom: LineString = row.geometry

        node_start, node_end = create_nodes_from_linestring(geom)

        # Absolutely critical. I don't know why set allows adding more than one identical node.
        # Perhaps they are not identical. TODO: Consider if there is a better way to check if a node was already added.
        if node_start.name in nodes_names:
            node_start = nodes[nodes_names.index(node_start.name)]
        else:
            nodes.append(node_start)
            nodes_names.append(node_start.name)
        if node_end.name in nodes_names:
            node_end = nodes[nodes_names.index(node_end.name)]
        else:
            nodes.append(node_end)
            nodes_names.append(node_end.name)

        edge = create_edge_from_linestring(geom, node_start, node_end)
        edge2 = create_edge_from_linestring(geom, node_end, node_start)

        edges.append(edge)
        edges.append(edge2)

    graph = Graph(list(nodes), list(edges))
    return graph


if __name__ == "__main__":
    filename = "shapefiles/Halinow Highways/Halinow Highways Latane.shp"
    load_shapefile(filename)
