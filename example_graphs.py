from classes.node import Node
from classes.edge import Edge
from classes.graph import Graph


def example_graph_1() -> tuple[Graph, Node, Node]:
    A: Node = Node("A", 0, 0)
    B: Node = Node("B", 1, 0)
    C: Node = Node("C", 0, 1)
    D: Node = Node("D", 1, 1)
    E: Node = Node("E", 2, 1)
    F: Node = Node("F", 2, 0)

    edges = [Edge(A, B, 1), Edge(A, C, 2), Edge(B, A, 1),
             Edge(B, D, 2), Edge(C, A, 2), Edge(C, D, 2),
             Edge(C, F, 6), Edge(D, B, 2), Edge(D, C, 2),
             Edge(D, E, 2), Edge(E, D, 2), Edge(E, F, 2),
             Edge(F, C, 6), Edge(F, E, 2)]

    nodes = [A, B, C, D, E, F]

    graph = Graph(nodes, edges)
    return graph, A, F


def example_graph_halinow() -> tuple[Graph, Node, Node]:
    from load_shapefile import load_shapefile
    graph: Graph = load_shapefile("shapefiles/Halinow Highways Latane/Halinow Highways Latane.shp")

    node_start: Node = graph.nodes[0]
    node_end: Node = graph.nodes[len(graph.nodes)//2]
    for node in graph.nodes:
        if node.y > node_start.y: node_start = node
        if node.y < node_end.y: node_end = node

    if node_start is node_end:
        raise RuntimeError()
    return graph, node_start, node_end
