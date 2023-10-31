from collections.abc import Callable

from classes.node import Node
from classes.priorityQueue import PriorityQueue


def a_star(start: Node, finish: Node, heuristic: Callable[[Node], float]) -> Node:
    open: PriorityQueue = PriorityQueue()
    closed: set[str] = set()

    start.g = 0
    start.f = start.g + heuristic(start)
    start.previous = None

    open.put(start, start.g)

    while not open.empty():
        current = open.get()

        if current.name in closed:
            continue

        if current is finish:
            break

        for neighbor in current.neighbours:
            neighbor_node: Node = neighbor.end
            cost_to_go_to_neighbor_node = neighbor.cost

            g = current.g + cost_to_go_to_neighbor_node
            f = g + heuristic(neighbor_node)
            if g < neighbor_node.g:
                neighbor_node.g = g
                neighbor_node.f = f
                neighbor_node.previous = current
                open.put(neighbor_node, f)

        closed.add(current.name)

    return finish
