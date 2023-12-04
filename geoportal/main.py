import time

from geoportal.algorithms.a_star import a_star
from geoportal.algorithms.algorithms import *
from geoportal.example_graphs import *


def distance(node: Node) -> float:
    return distance_between_nodes(node, finish_node)


if __name__ == '__main__':
    print("Preparing graph...")

    geofile = "IT CAN'T WORK IF YOU DON'T SPECIFY THE PATH, NOW, CAN IT?"
    start_time = time.time()
    graph, gdf, start_node, finish_node = create_example_graph_from_file(geofile)
    for node in graph.nodes:
        if node.y == 52.22607600097249 and node.x == 21.35621683116744:
            start_node = node
            print("rewritten start")
        elif node.y == 52.230504323308914 and node.x == 21.348326441290315:
            finish_node = node
            print("rewritten end")
    elapsed_time = time.time() - start_time

    print(f"{elapsed_time} has passed")
    print("Graph prepared, mapping route...")

    start_time = time.time()
    output = a_star(start_node, finish_node, distance, False)
    elapsed_time = time.time() - start_time

    print(f"{elapsed_time} has passed")
    print("Saving file...")

    path_gdf = output.get_path_gdf(gdf)
    path_gdf.to_file("path.geojson", driver="GeoJSON")

    path_gdf = output.get_path_gdf(gdf, get_linestrings=True)
    path_gdf.to_file("path_linestring.geojson", driver="GeoJSON")
