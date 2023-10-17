from classes.node import Node
from classes.edge import Edge
from algorithms.algorithms import *

A = Node("A", 0, 0)
B = Node("B", 1, 0)
C = Node("C", 0, 1)
D = Node("D", 1, 1)
E = Node("E", 2, 1)
F = Node("F", 2, 0)

A.add_neighbours([Edge(A, B, 1), Edge(A, C, 2)])
print(A)

B.add_neighbours([Edge(B, A, 1), Edge(B, D, 2)])
print(B)

C.add_neighbours([Edge(C, A, 2), Edge(C, D, 2), Edge(C, F, 6)])
print(C)

D.add_neighbours([Edge(D, B, 2), Edge(D, C, 2), Edge(D, E, 2)])
print(D)

E.add_neighbours([Edge(E, D, 2), Edge(E, F, 2)])
print(E)

F.add_neighbours([Edge(F, C, 6), Edge(F, E, 2)])
print(F)

if __name__ == '__main__':
    print()
    finish_node = F
    start_node = A


    def distance(node: Node) -> float:
        return distance_between_nodes(node, finish_node)


    output = a_star(start_node, finish_node, distance)

    print("Found path to:")
    print(output)
    print("The path being:")
    print(output.path())
