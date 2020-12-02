from typing import List
from app.constants import MapConstants
from scipy.spatial.distance import cdist
from ..models.universe_components import Planet

import numpy as np
import networkx as nx


def get_hyperlane_edges(hyperlanes: dict, planet_dict: dict) -> List[tuple]:
    """A Function that generates edges from hyperlane and planet data

    Args:
        hyperlanes (dict): A dictionary that holds hyperlanes with their planets
        planet_dict (dict): A dictionary that holds planet names and their information

    Yields:
        Iterator[tuple]: a touple with edge information an the route name
    """
    
    for route, planets in hyperlanes.items():
        planet_routes = get_planet_pair(planets)
        yield ((planet_dict[start],
                planet_dict[end],
                planet_dict[start].location.distance(planet_dict[end].location))
               for start, end in planet_routes), route


def get_planet_pair(planet_list: list):
    """A function that generates a list of pairs betwen planets

    Args:
        planet_list (list): planet name list

    Returns:
        list: A list of lists holding planet pairs
    """
    return list(zip(*[planet_list[index::1] for index in range(2)]))


def get_min_distance(source_group, source_positions, target_group, target_positions):
    """A function to get the closest objects between groups

    Args:
        source_group: a list of source objects
        source_positions: the position of the source objects
        target_group: a list of target objects
        target_positions: the position of the target objects

    Returns:
        tuple: the closest objects and the distance between them
    """
    distance_matrix = cdist(source_positions, target_positions)
    min_index = np.argmin(distance_matrix, axis=None)
    index = np.unravel_index(min_index, distance_matrix.shape)
    return source_group[index[0]], target_group[index[1]], distance_matrix[index]


def get_closest_planet_in_group(planet: Planet, planets, planets_positions):
    """A function to get the closest planet to another planet from a group

    Args:
        planet (Planet): the source planet
        planets (list): a group of planets we want to compare
        planets_positions (list): the positions of the group of planets

    Returns:
        [tuple]: the closest planet from the group and its distabce
    """
    start_position = np.array([[planet.location.x, planet.location.y]])
    _, target, distance = get_min_distance([planet], start_position, planets, planets_positions)
    return target, distance


def get_edges_to_hyperlane_planets(planet_list: set, planets_on_hyperlanes: set):
    """A function that generates graph edges between disconected planets and the closest
       planet in a hyperlane

    Args:
        planet_list (set): disconected planet set
        planets_on_hyperlanes (set): planets that are part of a hyperlane

    Yields:
        [tuple]: A planet pair and the distance between them
    """
    planet_set = planet_list.difference(planets_on_hyperlanes)
    planets_on_hyperlanes = np.asarray(list(planets_on_hyperlanes))
    if planets_on_hyperlanes.size != 0:
        hyperlanes_positions = np.asarray([[pl.location.x, pl.location.y] for pl in planets_on_hyperlanes])
        for planet in planet_set:
            closest, distance = get_closest_planet_in_group(planet, planets_on_hyperlanes, hyperlanes_positions)
            if distance <= MapConstants.GRID_SIDE:
                yield (closest, planet, distance*MapConstants.NO_HYPERLANE_DISTANCE_FACTOR)


def get_edges_to_isolates(isolate_planet_list: set, planets: set):
    """A function to connect planets that are to far to be part of a hyperlane or a grid

    Args:
        isolate_planet_list (set): the set of isolated planets
        planets (set): the set of planets with connections

    Yields:
        [tuple]: A planet pair and the distance between them 
    """
    connected_planets = np.asarray(list(planets.difference(isolate_planet_list)))
    connected_planets_positions = np.asarray([[pl.location.x, pl.location.y] for pl in connected_planets])
    for planet in isolate_planet_list:
        closest, distance = get_closest_planet_in_group(planet, connected_planets, connected_planets_positions)
        yield (closest, planet, distance*MapConstants.NO_HYPERLANE_DISTANCE_FACTOR)


def get_edges_for_graph_components(graph: nx.Graph):
    """A function to make edges between graph components just to make sure the graph is fully connected

    Args:
        graph (nx.Graph): the full graph representation of the map

    Yields:
        tuple: a planet pair and the distance between them
    """
    components = sorted(nx.connected_components(graph), key=len, reverse=True)
    component_planets = np.asarray(list(components[0]))
    component_planet_positions = np.asarray([[pl.location.x, pl.location.y] for pl in component_planets])
    for component in components[1:]:
        leftover_planets = np.asarray(list(component))
        leftover_planets_positions = np.asarray([[pl.location.x, pl.location.y] for pl in leftover_planets])
        source, target, distance = get_min_distance(component_planets, component_planet_positions, leftover_planets, leftover_planets_positions)
        yield (source, target, distance*MapConstants.NO_HYPERLANE_DISTANCE_FACTOR)
