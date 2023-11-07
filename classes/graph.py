from classes.edge import Edge
from classes.node import Node


class Graph:
    def __init__(self, nodes: list[Node], edges: list[Edge]):
        self.nodes: list[Node] = nodes
        self.edges: list[Edge] = edges
        for edge in self.edges:
            edge.start.add_neighbour(edge)

    def get_node(self, node_name: str) -> Node | None:
        for node in self.nodes:
            if node.name is node_name:
                return node
        return None

    def generate_nodes_geojson(self, filename_to_be_created: str) -> None:
        import geopandas as gpd
        x = []
        y = []
        for node in self.nodes:
            x.append(node.x)
            y.append(node.y)
        gdf = gpd.GeoDataFrame(
            geometry=gpd.points_from_xy(x, y),
            crs="EPSG:2180"
        )
        geojson = gdf.to_json(to_wgs84=True)
        with open(filename_to_be_created + ".geojson", "w") as geojson_file:
            geojson_file.write(geojson)
        return
