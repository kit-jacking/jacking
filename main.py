from algorithms.algorithms import *
from algorithms.a_star import a_star
from example_graphs import *

if __name__ == '__main__':
    print("Preparing graph...")
    graph, start_node, finish_node = example_graph_halinow()
    print("Graph prepared, starting on route")


    def distance(node: Node) -> float:
        return distance_between_nodes(node, finish_node)


    output = a_star(start_node, finish_node, distance)

    print("Found path to:")
    print(output)
    print("The path being::")
    print(output.path())

    output.save_path_geopandas_geojson("dataframe")
