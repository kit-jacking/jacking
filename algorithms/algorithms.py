import math
from classes.node import Node
from collections.abc import Callable
from classes.priorityQueue import PriorityQueue


def distance_between_points(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def distance_between_nodes(node1: Node, node2: Node) -> float:
    return distance_between_points(node1.x, node1.y, node2.x, node2.y)


def a_star(start: Node, finish: Node, heuristic: Callable[[Node], float]) -> Node:
    open = PriorityQueue()
    closed = set()

    start.g = 0
    start.f = start.g + heuristic(start)
    start.previous = None

    open.put(start, start.g)

    while not open.empty():
        current = open.get()

        if current is finish:
            break

        for neighbor in current.neighbours:
            neighbor_node: Node = neighbor[0]
            cost_to_go_to_neighbor_node = neighbor[1]

            g = current.g + cost_to_go_to_neighbor_node
            f = g + heuristic(neighbor_node)
            if g < neighbor_node.g:
                neighbor_node.g = g
                neighbor_node.f = f
                neighbor_node.previous = current
                open.put(neighbor_node, f)

        closed.add(current)

    return finish
