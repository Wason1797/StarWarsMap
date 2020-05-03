from typing import List
from itertools import chain
from ..models.universe_components import Region, Sector, Grid, Planet

import json


def get_region_db(db_path: str) -> List[Region]:
    db = json.load(open(db_path))
    return [Region(region,
                   [Sector(sector,
                           [Planet(planet['name'], planet['coords'], planet['is_canon'])
                            for planet in planets])
                    for sector, planets in sectors.items()])
            for region, sectors in db.items()]


def get_grid_db(db_path: str) -> List[Grid]:
    db = json.load(open(db_path))
    return [Grid(grid,
                 [Planet(planet['name'], planet['coords'], planet['is_canon'])
                  for planet in planets])
            for grid, planets in db.items()]


def get_hyperlanes(db_path: str) -> dict:
    return json.load(open(db_path))


def get_planets(regions: List[Region]) -> List[Planet]:
    return list(chain.from_iterable(region.planets for region in regions))
