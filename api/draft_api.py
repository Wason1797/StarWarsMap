from itertools import chain
from flask_cors import CORS
from flask import Flask, jsonify
from scripts.graph.transform_db_to_graph import get_region_db, get_hyperlanes


app = Flask(__name__)
CORS(app)


class MemoryDB:

    def __init__(self):
        region_path = './data/regions_db.json'
        hyperlanes_path = './data/hyperlanes_db.json'
        self.regions = get_region_db(region_path)
        self.planet_list = list(chain.from_iterable(region.planets for region in self.regions))
        hyperlanes_db = get_hyperlanes(hyperlanes_path)
        planet_search_dict = {planet.name: planet for planet in self.planet_list}

        self.hyperlanes = [{
            'name': name,
            'planets': [planet_search_dict[planet] for planet in planets]
        } for name, planets in hyperlanes_db.items()]


memory_db_instance = MemoryDB()


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = memory_db_instance.planet_list
    return jsonify([planet.to_dict() for planet in planets])


@app.route('/hyperlanes/points', methods=['GET'])
def get_hyperlane_points():
    hyperlanes = memory_db_instance.hyperlanes
    return jsonify(
        [{'name': lane.get('name'),
          'points': [(planet.location.x, planet.location.y) for planet in lane.get('planets')]}
         for lane in hyperlanes]
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
