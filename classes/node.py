import math


class Node:
    def __init__(self, name: str, x: float, y: float, neighbours: "list[tuple[Node, float]]" = None,
                 g: float = math.inf, f: float = math.inf, previous: "Node" = None):
        self.name: str = name
        self.x = x
        self.y = y

        if neighbours:
            self.neighbours: "list[tuple[Node, float]]" = neighbours
        else:
            self.neighbours: "list[tuple[Node, float]]" = []

        self.g = g
        self.f = f
        self.previous = previous

    def add_neighbour(self, node: "Node", cost: float):
        if node is not None and (node, cost) not in self.neighbours:
            self.neighbours.append((node, cost))

    def add_neighbours(self, nodes_and_costs: list[tuple["Node", float]]) -> None:
        if not nodes_and_costs:
            return
        for node, cost in nodes_and_costs:
            self.add_neighbour(node, cost)

    def path(self):
        if self.previous is None:
            return self.name

        return f"{self.name} -> " + self.previous.path()

    def __str__(self):
        return f"{self.name}({self.x}, {self.y}), neighbours: {[f'{node.name} cost: {cost}' for (node, cost) in self.neighbours]}"

    def __lt__(self, node: "Node"):
        if type(node) is not type(self):
            raise RuntimeError

        return self.f < node.f

    def copy(self):
        return Node(self.name, self.x, self.y, self.neighbours, self.g, self.f, self.previous)
