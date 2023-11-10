import geopandas as gpd
from shapely import LineString, MultiLineString

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
                                edge_id: int,
                                category: str) -> Edge:
    return Edge(node_start, node_end, linestring.length, edge_id, category=category)


def create_graph_and_geodataframe(file_to_load: str, crs: str = "epsg:4326",
                                  directions_column_name: str = "KIERUNKOWOSC") -> tuple[Graph, gpd.GeoDataFrame]:
    df = gpd.read_file(file_to_load)
    df.crs = crs

    nodes: list[Node] = []
    edges: list[Edge] = []
    conjunction_manager = ConjunctionManager()
    for i, row in df.iterrows():
        multilinestring = row.geometry.geom_type.startswith("MultiLineString")
        linestring = row.geometry.geom_type.startswith("LineString")
        if multilinestring:
            geom: MultiLineString = row.geometry.geoms[0]
        elif linestring:
            geom: LineString = row.geometry
        elif not linestring:
            print("Not linestring, nor multilinesetring: ", row.geometry.geom_type)
            continue

        probable_node_start, probable_node_end = create_nodes_from_linestring(geom)

        node_start = conjunction_manager.get_conjunction(probable_node_start)
        node_end = conjunction_manager.get_conjunction(probable_node_end)
        nodes.append(node_start)
        nodes.append(node_end)

        try:
            direction = row[directions_column_name]
        except:
            direction = 0

        if direction == 0:
            edge = create_edge_from_linestring(geom, node_start, node_end, i, row["KLASADROGI"])
            edge2 = create_edge_from_linestring(geom, node_end, node_start, i, row["KLASADROGI"])
            edges.append(edge)
            edges.append(edge2)
        elif direction == 1:
            edge = create_edge_from_linestring(geom, node_start, node_end, i, row["KLASADROGI"])
            edges.append(edge)
        elif direction == 2:
            edge2 = create_edge_from_linestring(geom, node_end, node_start, i, row["KLASADROGI"])
            edges.append(edge2)

    graph = Graph(list(nodes), list(edges))
    return graph, df


if __name__ == "__main__":
    filename = "shapefiles/Halinow Highways Latane/Halinow Highways Latane.shp"
    create_graph_and_geodataframe(filename, "epsg:4326")
