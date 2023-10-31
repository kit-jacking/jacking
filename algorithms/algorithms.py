import math

from classes.node import Node


def distance_between_points(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def distance_between_nodes(node1: Node, node2: Node) -> float:
    return distance_between_points(node1.x, node1.y, node2.x, node2.y)



