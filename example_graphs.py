import geopandas as gpd

from classes.edge import Edge
from classes.graph import Graph
from classes.node import Node


def example_graph_1() -> tuple[Graph, Node, Node]:
    A: Node = Node("A", 0, 0)
    B: Node = Node("B", 1, 0)
    C: Node = Node("C", 0, 1)
    D: Node = Node("D", 1, 1)
    E: Node = Node("E", 2, 1)
    F: Node = Node("F", 2, 0)

    edges = [Edge(A, B, 1), Edge(A, C, 2), Edge(B, A, 1),
             Edge(B, D, 2), Edge(C, A, 2), Edge(C, D, 2),
             Edge(C, F, 10, category='autostrada'), Edge(D, B, 2), Edge(D, C, 2),
             Edge(D, E, 2), Edge(E, D, 2), Edge(E, F, 2),
             Edge(F, C, 10, category='autostrada'), Edge(F, E, 2)]

    nodes = [A, B, C, D, E, F]

    graph = Graph(nodes, edges)
    return graph, C, F


def example_graph_shapefile(path: str) -> tuple[Graph, gpd.GeoDataFrame, Node, Node]:
    from load_shapefile import create_graph_and_geodataframe
    (graph, gdf) = create_graph_and_geodataframe(path)

    node_start: Node = graph.nodes[0]
    node_end: Node = graph.nodes[-1]
    for node in graph.nodes:
        if node.x > node_start.x: node_start = node
        if node.x < node_end.x: node_end = node

    if node_start is node_end:
        raise RuntimeError()
    return graph, gdf, node_start, node_end


def example_graph_halinow() -> tuple[Graph, gpd.GeoDataFrame, Node, Node]:
    return example_graph_shapefile("shapefiles/Halinow Highways Latane/Halinow Highways Latane.shp")
