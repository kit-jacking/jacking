from geoportal.classes.node import Node


class ConjunctionManager:
    def __init__(self):
        self.conjunctions: dict[tuple[float, float], Node] = dict()

    def get_conjunction(self, node: Node) -> Node:
        if not (node.x, node.y) in self.conjunctions.keys():
            self.conjunctions[(node.x, node.y)] = node
        return self.conjunctions[(node.x, node.y)]
