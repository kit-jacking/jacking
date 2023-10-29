from algorithms.algorithms import *
from example_graphs import example_graph_1, example_graph_halinow

# graph, start_node, finish_node = example_graph_1()
graph, start_node, finish_node = example_graph_halinow()

if __name__ == '__main__':
    def distance(node: Node) -> float:
        return distance_between_nodes(node, finish_node)

    output = a_star(start_node, finish_node, distance)

    print("Found path to:")
    print(output)
    print("The path being::")
    print(output.path())

    geojson = output.get_geopandas_geojson()
    # geojson = output.create_geojson()

    with open("output.geojson", "w") as geojson_file:
        geojson_file.write(geojson)
