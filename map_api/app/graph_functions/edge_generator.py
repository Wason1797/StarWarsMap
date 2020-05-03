from typing import List
from app.constants import MapConstants
from scipy.spatial.distance import cdist
from ..models.universe_components import Planet

import numpy as np
import networkx as nx


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
            if distance <= MapConstants.GRID_SIDE:
                yield (closest, planet, distance*MapConstants.NO_HYPERLANE_DISTANCE_FACTOR)


def get_edges_to_isolates(isolate_planet_list: set, planets: set):
    connected_planets = np.asarray(list(planets.difference(isolate_planet_list)))
    connected_planets_positions = np.asarray([[pl.location.x, pl.location.y] for pl in connected_planets])
    for planet in isolate_planet_list:
        closest, distance = get_closest_planet_in_group(planet, connected_planets, connected_planets_positions)
        yield (closest, planet, distance*MapConstants.NO_HYPERLANE_DISTANCE_FACTOR)


def get_edges_for_graph_components(graph: nx.Graph):
    components = sorted(nx.connected_components(graph), key=len, reverse=True)
    component_planets = np.asarray(list(components[0]))
    component_planet_positions = np.asarray([[pl.location.x, pl.location.y] for pl in component_planets])
    for component in components[1:]:
        leftover_planets = np.asarray(list(component))
        leftover_planets_positions = np.asarray([[pl.location.x, pl.location.y] for pl in leftover_planets])
        source, target, distance = get_min_distance(component_planets, component_planet_positions, leftover_planets, leftover_planets_positions)
        yield (source, target, distance*MapConstants.NO_HYPERLANE_DISTANCE_FACTOR)
