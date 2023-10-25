from classes.node import Node
from classes.priorityQueue import PriorityQueue

def dijkstra(source: Node, target: Node):
    
    pq = PriorityQueue()
    source.g = 0
    pq.put(source, source.g)
            
    while not pq.empty():
        curr_node = pq.get()
        
        if curr_node == target:
            break
        
        for e in curr_node.neighbours:
            new_cost = curr_node.g + e.cost
            if new_cost < e.end.g:
                e.end.g = new_cost
                e.end.previous = curr_node
                pq.put(e.end, new_cost)
                
    return target