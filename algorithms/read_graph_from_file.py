def read_graph(file: str):
    with open(file) as f:
        graph_raw = f.readlines()
        graph = []
        for i in graph_raw:
            graph.append(i.replace('\n', '').split('\t'))
        
        # TO DO
        # scan 4 directions of every number and add nodes and edges accordingly
            
    print(graph)