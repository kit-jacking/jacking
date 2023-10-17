from classes.node import Node
from algorithms.algorithms import *

A = Node("A", 0, 0)
B = Node("B", 1, 0)
C = Node("C", 0, 1)
D = Node("D", 1, 1)
E = Node("E", 2, 1)
F = Node("F", 2, 0)

A.add_neighbours([(B, 1), (C, 2)])
print(A)

B.add_neighbours([(A, 1), (D, 2)])
print(B)

C.add_neighbours([(A, 2), (D, 2), (F, 6)])
print(C)

D.add_neighbours([(B, 2), (C, 2), (E, 2)])
print(D)

E.add_neighbours([(D, 2), (F, 2)])
print(E)

F.add_neighbours([(C, 6), (E, 2)])
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

