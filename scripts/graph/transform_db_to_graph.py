from typing import List
from itertools import chain
from shapely.geometry import Polygon
from models.universe_components import Planet, Grid, Sector, Region

import json

import networkx as nx
import matplotlib.pyplot as plt


def plot_graph(graph, node_color=None):
    pos = {node: list(node.location.coords)[0] for node in graph.nodes()}
    nx.draw_networkx(graph, pos=pos, node_size=10, with_labels=False, node_color=node_color, font_size=8)


def get_region_db(db_path) -> List['Region']:
    db = json.load(open(db_path))
    return [Region(region,
                   [Sector(sector,
                           [Planet(planet['name'], planet['coords'])
                            for planet in planets])
                    for sector, planets in sectors.items()])
            for region, sectors in db.items()]


def get_grid_db(db_path) -> List['Grid']:
    db = json.load(open(db_path))
    return [Grid(grid,
                 [Planet(planet['name'], planet['coords'])
                  for planet in planets])
            for grid, planets in db.items()]


if __name__ == "__main__":
    region_path = 'D:/wason/Documents/Trabajos Universidad/Proyectos y Soluciones/StarWarsMap/data/regions_db.json'
    grid_path = 'D:/wason/Documents/Trabajos Universidad/Proyectos y Soluciones/StarWarsMap/data/grid_db.json'

    regions = get_region_db(region_path)
    grids = get_grid_db(grid_path)

    graph = nx.Graph()
    graph.add_nodes_from(chain.from_iterable(region.planets for region in regions))
    plot_graph(graph)

    for region in regions:
        if isinstance(region.shape, Polygon):
            plt.plot(*region.shape.exterior.xy)

    for grid in grids:
        if isinstance(grid.shape, Polygon):
            plt.plot(*grid.shape.exterior.xy)

    # for sector in chain.from_iterable(region.sectors for region in regions):
    #     shape = sector.shape.exterior.xy if isinstance(sector.shape, Polygon) else sector.shape.xy
    #     if sector.shape.area < 500000:
    #         plt.plot(*shape)
    #         plt.text(sector.shape.centroid.x, sector.shape.centroid.y, sector.name, fontsize=6)

    # for grid in chain.from_iterable(region.grids for region in regions):
    #     if isinstance(grid.shape, Polygon):
    #         plt.plot(*grid.shape.exterior.xy)
    #     else:
    #         plt.plot(*grid.shape.xy)
    plt.show()
