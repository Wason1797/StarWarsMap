from typing import List
from itertools import chain
from shapely.geometry import Polygon
from models.universe_components import Planet, Grid, Sector, Region

import json

import networkx as nx
import matplotlib.pyplot as plt

HYPERLANES = {
    'Rimma Trade Route': ['Abregado-rae', 'Dentaal', 'Giju',
                          'Ghorman', 'Vanik', 'Thyferra', 'Tauber', "Yag'Dhul", 'Sukkult',
                          'Wroona', 'Tregillis', 'Vandelhelm', 'Woostri', 'Daemen',
                          'Alakatha', 'Lanthe', 'Vondarc', 'Medth', 'Tshindral',
                          'Sullust', 'Eriadu', 'Bith', 'Triton', 'Praesitlyn', 'Sluis Van',
                          'Denab', 'Tarabba', 'Adarlon', 'Karideph', 'Pergitor', "Kal'Shebbol"],

    'Corellinan Run': ['Coruscant', 'Ixtlar', 'Corellia', 'Tinnel', 'Loronar', 'Byblos', 'Iseno',
                       'Denon', 'Spirana', 'Rhommamool', 'Allanteen', 'Gamor', 'Milagro', 'New Cov',
                       'Druckenwell', 'Mon Gazza', 'Herdessa', 'Radnor', 'Christophsis', 'Savareen',
                       'Ryloth', "Smuggler's Run"],

    'Corellian Trade Spine': ['Corellia', 'Hosnian Prime', 'Kelada', 'Foless', 'Mechis III', "Yag'Dhul", 'Harrin', 'Kinyen', 'Bomis Koori', 'Kriselist', 'Kaal', 'Jiroch', 'Mugaar', 'Gerrenthum',
                              'Isde Naha', "Berrol's Donn", 'Manpha', 'Terminus']
}


def plot_graph(graph, node_color=None):
    pos = {node: list(node.location.coords)[0] for node in graph.nodes()}
    nx.draw_networkx(graph, pos=pos, node_size=10, with_labels=False, node_color=node_color)


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


def get_planet_pair(planet_list: list):
    return list(zip(*[planet_list[index::1] for index in range(2)]))


if __name__ == "__main__":
    region_path = 'D:/wason/Documents/Trabajos Universidad/Proyectos y Soluciones/StarWarsMap/data/regions_db.json'
    grid_path = 'D:/wason/Documents/Trabajos Universidad/Proyectos y Soluciones/StarWarsMap/data/grid_db.json'

    regions = get_region_db(region_path)
    grids = get_grid_db(grid_path)
    planet_list = list(chain.from_iterable(region.planets for region in regions))

    planet_search_dict = {planet.name: planet for planet in planet_list}

    graph = nx.Graph()
    graph.add_nodes_from(planet_list)

    for route, planets in HYPERLANES.items():
        planet_routes = get_planet_pair(planets)
        edges = [(planet_search_dict[start],
                  planet_search_dict[end],
                  planet_search_dict[start].location.distance(planet_search_dict[end].location))
                 for start, end in planet_routes]

        graph.add_weighted_edges_from(edges, label=route)

    plot_graph(graph)

    for region in regions:
        if isinstance(region.shape, Polygon):
            plt.plot(*region.shape.exterior.xy)

    for grid in grids:
        if isinstance(grid.shape, Polygon):
            plt.plot(*grid.shape.exterior.xy)

    # for planet in nx.isolates(graph):
    #     plt.plot(*planet.location.coords)

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
