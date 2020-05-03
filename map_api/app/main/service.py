from flask import Blueprint, jsonify
from app.constants import Http
from .local_graph_storage import MemoryDB
from app.graph_functions.graph_factory import get_shortest_path


urls = Blueprint('urls', __name__)


@urls.route('/planets', methods=Http.GET)
def get_planets():
    planets = MemoryDB.get_storage().planet_list
    return jsonify([planet.to_dict() for planet in planets])


@urls.route('/hyperlanes/points', methods=Http.GET)
def get_hyperlane_points():
    hyperlanes = MemoryDB.get_storage().hyperlanes
    return jsonify(
        [{'name': lane.get('name'),
          'points': [(planet.location.x, planet.location.y) for planet in lane.get('planets')]}
         for lane in hyperlanes]
    )


@urls.route('/hyperlanes/shortest-path/points/<start>/<end>', methods=Http.GET)
def get_path(start: str, end: str):
    graph = MemoryDB.get_storage().graph
    planet_dict = MemoryDB.get_storage().planet_search_dict

    start = planet_dict.get(start)
    end = planet_dict.get(end)

    path = [(planet.location.x, planet.location.y)
            for planet in get_shortest_path(graph, start, end)] if start and end else []

    return jsonify(path)
