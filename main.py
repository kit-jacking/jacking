from algorithms.a_star import a_star
from algorithms.algorithms import *
from example_graphs import *


def distance(node: Node) -> float:
    return distance_between_nodes(node, finish_node)


if __name__ == '__main__':
    print("Preparing graph...")
    shp = "path/to/file/in/epsg:4326.geojson"
    graph, gdf, start_node, finish_node = example_graph_shapefile(shp)

    print("Graph prepared, starting on route")

    output = a_star(start_node, finish_node, distance, False)

    print("Found path to:")
    print(output)
    print("The path being::")
    print(output.path())

    path_gdf = output.get_path_gdf(gdf)
    path_gdf.to_file("outputs/path.geojson", driver="GeoJSON")
