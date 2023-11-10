from classes.node import Node
from classes.priorityQueue import PriorityQueue

def dijkstra(source: Node, target: Node, use_time_as_cost: bool = False):
    s = []
    pq = PriorityQueue()
    source.g = 0
    pq.put(source, source.g)
            
    while not pq.empty():
        curr_node = pq.get()
        
        if curr_node == target:
            break
        
        if curr_node in s:
            continue
        s.append(curr_node)
        
        for e in curr_node.neighbours:
            if use_time_as_cost:
                edge_cost = e.time
            else:
                edge_cost = e.length
            new_cost = curr_node.g + edge_cost
            if new_cost < e.end.g:
                e.end.g = new_cost
                e.end.previous = curr_node
                pq.put(e.end, new_cost)
                
    return target