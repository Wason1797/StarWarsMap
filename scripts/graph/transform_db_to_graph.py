from typing import List
from itertools import chain
from shapely.geometry import Polygon
from scipy.spatial.distance import cdist
from models.universe_components import Planet, Grid, Sector, Region

import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


ROUTE_COLOR = {
    'Rimma Trade Route': 'darkgreen',
    'Perlemian Trade Route': 'c',
    'Corellinan Run': 'maroon',
    'Corellian Trade Spine': 'violet',
    'Hydian Way': 'indigo',
    'No Hyperspace Lane': 'gray',
    "Elgit-M'Hanna Corridor": 'blue',
    "Reena Trade Route": "purple",
    "Bothan Run": 'green',
    "Guu Run": 'red',
    "Shipwrights' Trace": 'lightgreen',
    "Harrin Trade Corridor": 'darkblue',
    "Enarc Run": 'darkgray',
    "Gamor Run": 'darkcyan',
}


def plot_graph(graph, node_color=None):
    pos = {node: list(node.location.coords)[0] for node in graph.nodes()}
    edge_color = [edge[2] for edge in graph.edges.data('color')]
    nx.draw_networkx(graph, pos=pos, node_size=5, with_labels=False,
                     node_color=node_color, edge_color=edge_color, font_size=6)


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


def get_hyperlanes(db_path) -> dict:
    return json.load(open(db_path))


def get_hyperlane_edges(hyperlanes: dict) -> List[tuple]:
    for route, planets in hyperlanes.items():
        planet_routes = get_planet_pair(planets)
        yield ((planet_search_dict[start],
                planet_search_dict[end],
                planet_search_dict[start].location.distance(planet_search_dict[end].location))
               for start, end in planet_routes), route


def get_planet_pair(planet_list: list):
    return list(zip(*[planet_list[index::1] for index in range(2)]))


def get_closest_planet_in_hyperlane(planet: Planet, hyperlane_planets, hyperlane_positions):
    start_position = np.array([[planet.location.x, planet.location.y]])
    distance_matrix = cdist(start_position, hyperlane_positions)
    min_index = np.argmin(distance_matrix, axis=None)
    index = np.unravel_index(min_index, distance_matrix.shape)
    return hyperlane_planets[index[1]], distance_matrix[index]


def get_edges_to_hyperlane_planets(planet_list: set, planets_on_hyperlanes: set):
    planet_set = planet_list.difference(planets_on_hyperlanes)
    planets_on_hyperlanes = np.asarray(list(planets_on_hyperlanes.intersection(planet_list)))
    if planets_on_hyperlanes.size != 0:
        hyperlanes_positions = np.asarray([[pl.location.x, pl.location.y] for pl in planets_on_hyperlanes])
        for planet in planet_set:
            closest, distance = get_closest_planet_in_hyperlane(planet, planets_on_hyperlanes, hyperlanes_positions)
            yield (closest, planet, distance)


if __name__ == "__main__":
    region_path = 'D:/wason/Documents/Trabajos Universidad/Proyectos y Soluciones/StarWarsMap/data/regions_db.json'
    grid_path = 'D:/wason/Documents/Trabajos Universidad/Proyectos y Soluciones/StarWarsMap/data/grid_db.json'
    hyperlanes_path = 'D:/wason/Documents/Trabajos Universidad/Proyectos y Soluciones/StarWarsMap/data/hyperlanes_db.json'

    regions = get_region_db(region_path)
    grids = get_grid_db(grid_path)
    hyperlanes = get_hyperlanes(hyperlanes_path)
    hyperlane_edges = get_hyperlane_edges(hyperlanes)
    planet_list = list(chain.from_iterable(region.planets for region in regions))

    planet_search_dict = {planet.name: planet for planet in planet_list}
    planets_on_hyperlanes = {planet_search_dict[planet] for planet in chain.from_iterable(hyperlanes.values())}
    print(len(planets_on_hyperlanes))
    print(len(planet_search_dict))

    graph = nx.Graph()
    graph.add_nodes_from(set(planet_list))

    for edges, route in hyperlane_edges:
        graph.add_weighted_edges_from(edges, label=route, color=ROUTE_COLOR.get(route, 'darkblue'))

    for grid in grids:
        route = 'No Hyperspace Lane'
        graph.add_weighted_edges_from(get_edges_to_hyperlane_planets({planet_search_dict[pl.name] for pl in grid.planets},
                                                                     planets_on_hyperlanes),
                                      label=route, color=ROUTE_COLOR[route])

    print(len(list(nx.isolates(graph))))
    plot_graph(graph)

    # for region in regions:
    #     if isinstance(region.shape, Polygon):
    #         plt.plot(*region.shape.exterior.xy, linewidth=0.5)

    for grid in grids:
        if isinstance(grid.shape, Polygon):
            plt.plot(*grid.shape.exterior.xy, linewidth=1, color='lightgray')

    path_plot = get_planet_pair(nx.shortest_path(graph, planet_search_dict['Tatooine'], planet_search_dict['Felucia']))

    for start_planet, end_planet in path_plot:
        plt.plot([start_planet.location.x, end_planet.location.x],
                 [start_planet.location.y, end_planet.location.y], linewidth=2, color='red')

    plt.axis('off')
    plt.show()
