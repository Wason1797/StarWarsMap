from shapely.geometry import Polygon

import networkx as nx
import matplotlib.pyplot as plt


def plot_graph(graph: nx.Graph, node_color=None):
    pos = {node: list(node.location.coords)[0] for node in graph.nodes()}
    edge_color = [edge[2] for edge in graph.edges.data('color')]
    nx.draw_networkx(graph, pos=pos, node_size=5, with_labels=False,
                     node_color=node_color, edge_color=edge_color, font_size=6)


def plot_path(path: list):
    for start_planet, end_planet in path:
        plt.plot([start_planet.location.x, end_planet.location.x],
                 [start_planet.location.y, end_planet.location.y], linewidth=2, color='red')


def plot_map(graph: nx.Graph, path: list = None, grids=None, regions=None):
    plot_graph(graph)

    if regions:
        for region in regions:
            if isinstance(region.shape, Polygon):
                plt.plot(*region.shape.exterior.xy, linewidth=0.5)

    if grids:
        for grid in grids:
            if isinstance(grid.shape, Polygon):
                plt.plot(*grid.shape.exterior.xy, linewidth=0.5, color='gray')

    if path:
        plot_path(path)

    plt.axis('off')
    plt.show()
