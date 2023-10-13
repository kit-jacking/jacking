from classes.node import Node
from algorithms.algorithms import *

A = Node("A", 0, 0)
B = Node("B", 1, 0)
C = Node("C", 0, 1)
D = Node("D", 1, 1)
E = Node("E", 2, 1)
F = Node("F", 2, 0)
A.add_neighbour(B, 1)
A.add_neighbour(C, 2)
print(A)
B.add_neighbour(A, 1)
B.add_neighbour(D, 2)
print(B)
C.add_neighbour(A, 2)
C.add_neighbour(D, 2)
C.add_neighbour(F, 6)
print(C)
D.add_neighbour(B, 2)
D.add_neighbour(C, 2)
D.add_neighbour(E, 2)
print(D)
E.add_neighbour(D, 2)
E.add_neighbour(F, 2)
print(E)
F.add_neighbour(C, 6)
F.add_neighbour(E, 2)
print(F)

if __name__ == '__main__':
    print()
    finish_node = F
    start_node = A


    def distance(node: Node) -> float:
        return distance_between_nodes(node, finish_node)


    output = a_star(start_node, finish_node, distance)

    print(output)
    print(output.previous)
