from itertools import chain
from typing import List, Union
from functools import lru_cache
from shapely.geometry import Point, MultiPoint, Polygon
from app.constants import MapConstants


class Planet:
    def __init__(self, name: str, location: Union[Point, List[float]], is_canon: bool = True):
        self.name = name
        self.location = location if isinstance(location, Point) else Point(location)
        self.is_canon = is_canon

    @lru_cache()
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'location': [self.location.x, self.location.y],
            'is_canon': self.is_canon
        }

    def __repr__(self):
        return self.name


class Grid:
    color = 'gray'

    def __init__(self, name: str, planets: List['Planet']):
        self.name = name
        self.planets = planets

    @property
    @lru_cache()
    def shape(self) -> Polygon:
        letter, number = self.name.split('-')
        grid_side = MapConstants.GRID_SIDE
        letter_value = MapConstants.GRID_AlPHABET_TRANSFORM[letter]*grid_side
        number_value = MapConstants.GRID_NUMBER_TRANSFORM[int(number)]*grid_side
        return MultiPoint([(letter_value, number_value),
                           (letter_value+grid_side, number_value),
                           (letter_value, number_value+grid_side),
                           (letter_value+grid_side, number_value+grid_side)]).convex_hull

    @lru_cache()
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'color': self.color,
            'planets': [planet.to_dict() for planet in self.planets],
            'shape': list(self.shape.exterior.coords)
        }

    def __repr__(self):
        return self.name


class Sector:
    def __init__(self, name: str, planets: List['Planet']):
        self.name = name
        self.planets = planets

    @property
    @lru_cache()
    def shape(self) -> Polygon:
        return MultiPoint([planet.location for planet in self.planets]).convex_hull.buffer(2.5)

    def __repr__(self):
        return self.name

    @lru_cache()
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'planets': [planet.to_dict() for planet in self.planets],
            'shape': list(self.shape.exterior.coords)
        }


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
    def shape(self) -> Polygon:
        return MultiPoint([planet.location for planet in self.planets]).convex_hull.buffer(5)

    @lru_cache()
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'planets': [planet.to_dict() for planet in self.planets],
            'sectors': [sector.to_dict() for sector in self.sectors],
            'shape': list(self.shape.exterior.coords)
        }

    def __repr__(self):
        return self.name
