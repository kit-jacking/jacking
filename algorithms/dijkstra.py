from classes.graph import Graph
from classes.edge import Edge
from classes.node import Node
from classes.priorityQueue import PriorityQueue
import math


def dijkstra_full(graph: Graph, source: Node):
    distances_dict = {}
    previous_dict = {} # node: previous node
    pq = PriorityQueue()

    for node in graph.nodes:
        distance = 0 if node == source else math.inf
        distances_dict[node.name] = distance
        previous_dict[node.name] = -1
        pq.put(node, distances_dict[node.name])
    # brak trasy - graf niespojny dodac test
    while not pq.empty():
        curr_node = pq.get()
        print(curr_node.name)
        # if is target
        for e in curr_node.neighbours:
            if distances_dict[e.end.name] > distances_dict[curr_node.name] + e.cost:
                distances_dict[e.end.name] = distances_dict[curr_node.name] + e.cost
                previous_dict[e.end.name] = curr_node
                
    return distances_dict

# def dijkstra_target(graph: Graph, source: Node, target: Node):
#     visited = []
#     distances_dict = {source.name: 0}
#     previous_dict = {} # node: previous node
#     pq = PriorityQueue().put(source, distances_dict[source.name])
    
#     while True:
#         if pq.empty():
#             return -1
#         curr_node = pq.get()
#         if curr_node == target:
#             break
#         for e in curr_node.neighbours:
#             print('1')

                
#     return distances_dict
        