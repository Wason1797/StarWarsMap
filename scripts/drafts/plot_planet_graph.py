from typing import List
from functools import lru_cache
from shapely.geometry import Point, MultiPoint, Polygon


import json
import networkx as nx
import matplotlib.pyplot as plt


class Planet:
    def __init__(self, name: str, location: Point, is_canon: bool = True):
        self.name = name
        self.location = location
        self.is_canon = is_canon

    def __repr__(self):
        return self.name


class Grid:
    def __init__(self, name: str, planets: List['Planet']):
        self.name = name
        self.planets = planets

    @property
    @lru_cache()
    def shape(self):
        return MultiPoint([planet.location for planet in self.planets]).convex_hull


def plot_graph(graph, node_color=None):
    pos = {node: list(node.location.coords)[0] for node in graph.nodes()}
    nx.draw_networkx(graph, pos=pos, node_size=10, with_labels=True, node_color=node_color, font_size=8)


def get_grids(planet_database: dict, planet_coords: dict):
    search_planet = {name.lower().strip(): coords for name, coords in planet_coords.items()}
    for regions in planet_database.values():
        for sector_names in regions.values():
            for sectors in sector_names.values():
                for grid_names in sectors.values():
                    for grid in grid_names.values():
                        for grid_name, grid_components in grid.items():
                            planets = [Planet(planet, Point(search_planet.get(planet.lower().strip())))
                                       for planet in grid_components['planets'] if search_planet.get(planet.lower().strip())]
                            if planets:
                                yield Grid(grid_name, planets)


if __name__ == "__main__":
    planet_db = json.load(open('data/formatted_planet_db.json'))
    planet_coords = json.load(open('data/planet_coords.json'))

    graph = nx.Graph()
    graph.add_nodes_from([Planet(planet.lower().strip(), Point(coords))
                          for planet, coords in planet_coords.items() if len(coords) == 2])

    plot_graph(graph)
    grids = get_grids(planet_db, planet_coords)
    for grid in grids:
        if isinstance(grid.shape, Polygon):
            plt.plot(*grid.shape.exterior.xy)
    plt.axis('off')
    plt.show()
