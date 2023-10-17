from classes.node import Node
from classes.edge import Edge
from classes.graph import Graph
from algorithms.algorithms import *

A = Node("A", 0, 0)
B = Node("B", 1, 0)
C = Node("C", 0, 1)
D = Node("D", 1, 1)
E = Node("E", 2, 1)
F = Node("F", 2, 0)

edges = [Edge(A, B, 1), Edge(A, C, 2), Edge(B, A, 1),
         Edge(B, D, 2), Edge(C, A, 2), Edge(C, D, 2),
         Edge(C, F, 6), Edge(D, B, 2), Edge(D, C, 2),
         Edge(D, E, 2), Edge(E, D, 2), Edge(E, F, 2),
         Edge(F, C, 6), Edge(F, E, 2)]

nodes = [A, B, C, D, E, F]

graph = Graph(nodes, edges)

print(F)

if __name__ == '__main__':
    print()
    start_node = graph.nodes[graph.nodes.index(A)]
    finish_node = graph.nodes[graph.nodes.index(F)]


    def distance(node: Node) -> float:
        return distance_between_nodes(node, finish_node)


    output = a_star(start_node, finish_node, distance)

    print("Found path to:")
    print(output)
    print("The path being:")
    print(output.path())
