from itertools import chain
from typing import List, Tuple
from shapely.geometry import Polygon
from scipy.spatial.distance import cdist
from models.universe_components import Planet, Grid, Sector, Region, GRID_SIDE

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
    "Elgit-M'Hanna Corridor": 'blue',
    "Reena Trade Route": "purple",
    "Bothan Run": 'green',
    "Guu Run": 'orange',
    "Shipwrights' Trace": 'lightgreen',
    "Harrin Trade Corridor": 'darkblue',
    "Enarc Run": 'k',
    "Gamor Run": 'darkcyan',
}

NO_HYPERLANE_DISTANCE_FACTOR = 1000


def plot_graph(graph: nx.Graph, node_color=None):
    pos = {node: list(node.location.coords)[0] for node in graph.nodes()}
    edge_color = [edge[2] for edge in graph.edges.data('color')]
    nx.draw_networkx(graph, pos=pos, node_size=5, with_labels=False,
                     node_color=node_color, edge_color=edge_color, font_size=6)


def get_region_db(db_path: str) -> List['Region']:
    db = json.load(open(db_path))
    return [Region(region,
                   [Sector(sector,
                           [Planet(planet['name'], planet['coords'])
                            for planet in planets])
                    for sector, planets in sectors.items()])
            for region, sectors in db.items()]


def get_grid_db(db_path: str) -> List['Grid']:
    db = json.load(open(db_path))
    return [Grid(grid,
                 [Planet(planet['name'], planet['coords'])
                  for planet in planets])
            for grid, planets in db.items()]


def get_hyperlanes(db_path: str) -> dict:
    return json.load(open(db_path))


def get_planets(regions: List[Region]) -> List[Planet]:
    return list(chain.from_iterable(region.planets for region in regions))


def get_hyperlane_edges(hyperlanes: dict, planet_dict: dict) -> List[tuple]:
    for route, planets in hyperlanes.items():
        planet_routes = get_planet_pair(planets)
        yield ((planet_dict[start],
                planet_dict[end],
                planet_dict[start].location.distance(planet_dict[end].location))
               for start, end in planet_routes), route


def get_planet_pair(planet_list: list):
    return list(zip(*[planet_list[index::1] for index in range(2)]))


def get_min_distance(source_group, source_positions, target_group, target_positions):
    distance_matrix = cdist(source_positions, target_positions)
    min_index = np.argmin(distance_matrix, axis=None)
    index = np.unravel_index(min_index, distance_matrix.shape)
    return source_group[index[0]], target_group[index[1]], distance_matrix[index]


def get_closest_planet_in_group(planet: Planet, planets, planets_positions):
    start_position = np.array([[planet.location.x, planet.location.y]])
    _, target, distance = get_min_distance([planet], start_position, planets, planets_positions)
    return target, distance


def get_edges_to_hyperlane_planets(planet_list: set, planets_on_hyperlanes: set):
    planet_set = planet_list.difference(planets_on_hyperlanes)
    planets_on_hyperlanes = np.asarray(list(planets_on_hyperlanes))
    if planets_on_hyperlanes.size != 0:
        hyperlanes_positions = np.asarray([[pl.location.x, pl.location.y] for pl in planets_on_hyperlanes])
        for planet in planet_set:
            closest, distance = get_closest_planet_in_group(planet, planets_on_hyperlanes, hyperlanes_positions)
            if distance <= GRID_SIDE:
                yield (closest, planet, distance*NO_HYPERLANE_DISTANCE_FACTOR)


def get_edges_to_isolates(isolate_planet_list: set, planets: set):
    connected_planets = np.asarray(list(planets.difference(isolate_planet_list)))
    connected_planets_positions = np.asarray([[pl.location.x, pl.location.y] for pl in connected_planets])
    for planet in isolate_planet_list:
        closest, distance = get_closest_planet_in_group(planet, connected_planets, connected_planets_positions)
        yield (closest, planet, distance*NO_HYPERLANE_DISTANCE_FACTOR)


def get_edges_for_graph_components(graph: nx.Graph):
    components = sorted(nx.connected_components(graph), key=len, reverse=True)
    component_planets = np.asarray(list(components[0]))
    component_planet_positions = np.asarray([[pl.location.x, pl.location.y] for pl in component_planets])
    for component in components[1:]:
        leftover_planets = np.asarray(list(component))
        leftover_planets_positions = np.asarray([[pl.location.x, pl.location.y] for pl in leftover_planets])
        source, target, distance = get_min_distance(component_planets, component_planet_positions, leftover_planets, leftover_planets_positions)
        yield (source, target, distance*NO_HYPERLANE_DISTANCE_FACTOR)


def plot_map(graph: nx.Graph, grids=None, regions=None):
    plot_graph(graph)

    if regions:
        for region in regions:
            if isinstance(region.shape, Polygon):
                plt.plot(*region.shape.exterior.xy, linewidth=0.5)

    if grids:
        for grid in grids:
            if isinstance(grid.shape, Polygon):
                plt.plot(*grid.shape.exterior.xy, linewidth=0.5, color='gray')


def plot_path(path: list):
    for start_planet, end_planet in path:
        plt.plot([start_planet.location.x, end_planet.location.x],
                 [start_planet.location.y, end_planet.location.y], linewidth=2, color='red')


def generate_connected_graph(planet_list: List[Planet], hyperlanes: dict) -> Tuple[nx.Graph, dict]:

    planet_search_dict = {planet.name: planet for planet in planet_list}
    planets_on_hyperlanes = {planet_search_dict[planet] for planet in chain.from_iterable(hyperlanes.values())}
    print(f"Total Planets in map {len(planet_search_dict)}")
    print(f"Planets on hyperlanes {len(planets_on_hyperlanes)}")

    graph = nx.Graph()
    graph.add_nodes_from(set(planet_list))

    hyperlane_edges = get_hyperlane_edges(hyperlanes, planet_search_dict)
    for edges, route in hyperlane_edges:
        graph.add_weighted_edges_from(edges, label=route, color=ROUTE_COLOR.get(route, 'darkblue'))

    graph.add_weighted_edges_from(get_edges_to_hyperlane_planets(set(planet_list),
                                                                 planets_on_hyperlanes),
                                  label='No Hyperspace Lane', color='lightgray')

    isolated_planets = set(nx.isolates(graph))
    print(f"Planets with no connections {len(isolated_planets)}")

    graph.add_weighted_edges_from(get_edges_to_isolates(isolated_planets, set(graph.nodes)),
                                  label="Last Resort Route", color='yellow')

    graph.add_weighted_edges_from(get_edges_for_graph_components(graph),
                                  label="Component Artificial Route", color='purple')

    return graph, planet_search_dict


def get_shortest_path(graph: nx.Graph, start: Planet, end: Planet, pairs=False):
    path = nx.shortest_path(graph, start, end, weight='weight')
    return get_planet_pair(path) if pairs else path


if __name__ == "__main__":
    region_path = './data/regions_db.json'
    grid_path = './data/grid_db.json'
    hyperlanes_path = './data/hyperlanes_db.json'

    regions = get_region_db(region_path)
    grids = get_grid_db(grid_path)
    hyperlanes = get_hyperlanes(hyperlanes_path)

    planet_list = get_planets(regions)
    graph, planet_search_dict = generate_connected_graph(planet_list, hyperlanes)

    print(len(list(nx.connected_components(graph))))
    plot_map(graph, grids)

    path_plot = get_shortest_path(graph, planet_search_dict["Coruscant"], planet_search_dict["Jakku"])

    plot_path(path_plot)

    plt.axis('off')
    plt.show()
