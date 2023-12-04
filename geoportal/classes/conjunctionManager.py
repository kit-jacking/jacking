from geoportal.classes.node import Node
from collections.abc import Callable


class ConjunctionManager:
    def __init__(self):
        self.conjunctions: dict[tuple[float, float], Node] = dict()

    def get_conjunction(self, node: Node,
                        node_namer_function: Callable[[tuple[float, float]], str],
                        round_to: int = 6) -> Node:
        if not (node.x, node.y) in self.conjunctions.keys():
            rounded_x = round(node.x, round_to)
            rounded_y = round(node.y, round_to)
            rounded_name = node_namer_function((rounded_x, rounded_y))
            rounded_node = Node(rounded_name, rounded_x, rounded_y)
            self.conjunctions[(node.x, node.y)] = rounded_node
        return self.conjunctions[(node.x, node.y)]
