from collections.abc import Callable

from classes.node import Node
from classes.edge import Edge
from classes.priorityQueue import PriorityQueue


def a_star(start: Node, finish: Node, heuristic: Callable[[Node], float], use_time_as_cost: bool = False) -> Node:
    highway_speed = Edge.category_speed_dict['autostrada']
    heuristic_divider = highway_speed if use_time_as_cost else 1
    open: PriorityQueue = PriorityQueue()
    closed: set[str] = set()
    start.g = 0
    start.f = start.g + heuristic(start) / heuristic_divider
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
            if use_time_as_cost:
                cost_to_go_to_neighbor_node = neighbor.time
            else:
                cost_to_go_to_neighbor_node = neighbor.length

            g = current.g + cost_to_go_to_neighbor_node
            f = g + heuristic(neighbor_node) / heuristic_divider
            if g < neighbor_node.g:
                neighbor_node.g = g
                neighbor_node.f = f
                neighbor_node.previous = current, neighbor
                open.put(neighbor_node, f)

        closed.add(current.name)

    return finish
