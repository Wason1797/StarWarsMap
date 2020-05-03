class Http:
    GET = ['GET']
    POST = ['POST']
    PUT = ['PUT']
    PATCH = ['PATCH']
    DELETE = ['DELETE']


class MapConstants:
    GRID_AlPHABET_TRANSFORM = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWX', range(-11, 13)))
    GRID_NUMBER_TRANSFORM = dict(zip(range(1, 23), range(8, -13, -1)))
    GRID_SIDE = 100
    NO_HYPERLANE_DISTANCE_FACTOR = 1000
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


class DataConstants:
    REGIONS_PATH = './data/regions_db.json'
    HYPERLANES_PATH = './data/hyperlanes_db.json'
    GRIDS_PATH = './data/grid_db.json'
    CSV_DATABASE = './data/planets.csv'
