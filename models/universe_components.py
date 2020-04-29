from itertools import chain
from typing import List, Union
from functools import lru_cache
from shapely.geometry import Point, MultiPoint

GRID_AlPHABET_TRANSFORM = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWX', range(-11, 13)))
GRID_NUMBER_TRANSFORM = dict(zip(range(1, 23), range(8, -13, -1)))
GRID_SIDE = 100


class Planet:
    def __init__(self, name: str, location: Union[Point, List[float]], is_canon: bool = True):
        self.name = name
        self.location = location if isinstance(location, Point) else Point(location)
        self.is_canon = is_canon

    def __repr__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'location': [self.location.x, self.location.y],
            'is_canon': self.is_canon
        }


class Grid:
    def __init__(self, name: str, planets: List['Planet']):
        self.name = name
        self.planets = planets

    @property
    @lru_cache()
    def shape(self):
        letter, number = self.name.split('-')
        letter_value = GRID_AlPHABET_TRANSFORM[letter]*GRID_SIDE
        number_value = GRID_NUMBER_TRANSFORM[int(number)]*GRID_SIDE
        return MultiPoint([(letter_value, number_value),
                           (letter_value+GRID_SIDE, number_value),
                           (letter_value, number_value+GRID_SIDE),
                           (letter_value+GRID_SIDE, number_value+GRID_SIDE)]).convex_hull

    def __repr__(self):
        return self.name


class Sector:
    def __init__(self, name: str, planets: List['Planet']):
        self.name = name
        self.planets = planets

    @property
    @lru_cache()
    def shape(self):
        return MultiPoint([planet.location for planet in self.planets]).convex_hull.buffer(2.5)

    def __repr__(self):
        return self.name


class Region:
    def __init__(self, name: str, sectors: List['Sector']):
        self.name = name
        self.sectors = sectors

    @property
    @lru_cache()
    def planets(self):
        return list(chain.from_iterable(sector.planets
                                        for sector in self.sectors))

    @property
    @lru_cache()
    def shape(self):
        return MultiPoint([planet.location for planet in self.planets]).convex_hull.buffer(10)

    def __repr__(self):
        return self.name
