from flask_cors import CORS
from flask import Flask, jsonify
import scripts.graph.transform_db_to_graph as GraphFunctions


app = Flask(__name__)
CORS(app)


class MemoryDB:

    def __init__(self):
        region_path = './data/regions_db.json'
        hyperlanes_path = './data/hyperlanes_db.json'
        self.regions = GraphFunctions.get_region_db(region_path)
        self.planet_list = GraphFunctions.get_planets(self.regions)
        hyperlanes_db = GraphFunctions.get_hyperlanes(hyperlanes_path)
        self.graph, self.planet_search_dict = GraphFunctions.generate_connected_graph(self.planet_list, hyperlanes_db)

        self.hyperlanes = [{
            'name': name,
            'planets': [self.planet_search_dict[planet] for planet in planets]
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


@app.route('/hyperlanes/shortest-path/points/<start>/<end>', methods=['GET'])
def get_path(start: str, end: str):
    graph = memory_db_instance.graph
    planet_dict = memory_db_instance.planet_search_dict

    start = planet_dict.get(start)
    end = planet_dict.get(end)

    path = [(planet.location.x, planet.location.y)
            for planet in GraphFunctions.get_shortest_path(graph, start, end)] if start and end else []

    return jsonify(path)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
