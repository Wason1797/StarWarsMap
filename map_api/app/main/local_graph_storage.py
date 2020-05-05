from app.constants import DataConstants
from app.graph_functions.graph_factory import generate_connected_graph
from app.migrations.build_local_db import get_region_db, get_planets, get_hyperlanes, get_grid_db


class MemoryDB:

    storage = None

    def __init__(self):
        region_path = DataConstants.REGIONS_PATH
        hyperlanes_path = DataConstants.HYPERLANES_PATH
        self.regions = get_region_db(region_path)
        self.planet_list = get_planets(self.regions)
        self.grids = get_grid_db(DataConstants.GRIDS_PATH)
        self.hyperlanes_db = get_hyperlanes(hyperlanes_path)
        self.graph, self.planet_search_dict = generate_connected_graph(self.planet_list, self.hyperlanes_db)

        self.hyperlanes = [{
            'name': name,
            'planets': [self.planet_search_dict[planet] for planet in planets]
        } for name, planets in self.hyperlanes_db.items()]

    @classmethod
    def get_storage(cls) -> 'MemoryDB':
        cls.init_storage()
        return cls.storage

    @classmethod
    def init_storage(cls):
        if cls.storage is None:
            cls.storage = MemoryDB()
