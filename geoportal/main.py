import time

from geoportal.algorithms.a_star import a_star
from geoportal.algorithms.algorithms import *
from geoportal.example_graphs import *


def distance(node: Node) -> float:
    return distance_between_nodes(node, finish_node)


if __name__ == '__main__':
    print("Preparing graph...")

    geofile = "PROVIDE A PATH"

    start_time = time.time()
    graph, gdf, start_node, finish_node = create_example_graph_from_file(geofile)
    elapsed_time = time.time() - start_time

    print(f"{elapsed_time} has passed")
    print("Graph prepared, mapping route...")

    start_time = time.time()
    output: Node = a_star(start_node, finish_node, distance, False)
    elapsed_time = time.time() - start_time

    print(f"Length in CRS EPSG:2180 = {round(output.get_path_length(gdf, length_crs='EPSG:2180'), 3)} m")
    print(f"{elapsed_time} has passed")
    print("Saving file...")

    path_gdf = output.get_path_gdf(gdf)
    path_gdf.to_file("path.geojson", driver="GeoJSON")

    path_gdf = output.get_path_gdf(gdf, get_linestrings=True)
    path_gdf.to_file("path_linestring.geojson", driver="GeoJSON")
