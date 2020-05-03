from itertools import chain
from typing import List, Tuple
from .plot_graph import plot_map
from ..models.universe_components import Planet
from app.constants import MapConstants, DataConstants
from ..migrations.build_local_db import get_grid_db, get_hyperlanes, get_planets, get_region_db
from .edge_generator import get_hyperlane_edges, get_edges_to_hyperlane_planets, get_edges_to_isolates, \
    get_edges_for_graph_components, get_planet_pair

import networkx as nx


def generate_connected_graph(planet_list: List[Planet], hyperlanes: dict) -> Tuple[nx.Graph, dict]:

    planet_search_dict = {planet.name: planet for planet in planet_list}
    planets_on_hyperlanes = {planet_search_dict[planet] for planet in chain.from_iterable(hyperlanes.values())}
    print(f"Total Planets in map {len(planet_search_dict)}")
    print(f"Planets on hyperlanes {len(planets_on_hyperlanes)}")

    graph = nx.Graph()
    graph.add_nodes_from(set(planet_list))

    hyperlane_edges = get_hyperlane_edges(hyperlanes, planet_search_dict)
    for edges, route in hyperlane_edges:
        graph.add_weighted_edges_from(edges, label=route, color=MapConstants.ROUTE_COLOR.get(route, 'darkblue'))

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


def build_and_plot_test_graph():
    region_path = DataConstants.REGIONS_PATH
    grid_path = DataConstants.GRIDS_PATH
    hyperlanes_path = DataConstants.HYPERLANES_PATH

    regions = get_region_db(region_path)
    grids = get_grid_db(grid_path)
    hyperlanes = get_hyperlanes(hyperlanes_path)

    planet_list = get_planets(regions)
    graph, planet_search_dict = generate_connected_graph(planet_list, hyperlanes)

    path_plot = get_shortest_path(graph, planet_search_dict["Coruscant"], planet_search_dict["Jakku"], pairs=True)

    plot_map(graph, path=path_plot, grids=grids)
