from flask.cli import FlaskGroup

from app import flask_app
from app.graph_functions.graph_factory import get_shortest_path, plot_map
from app.main.local_graph_storage import MemoryDB

flask_app.app_context().push()

manager = FlaskGroup(flask_app)


@manager.command
def migrateup():
    pass


@manager.command('plotgraph')
def plotgraph():
    graph = MemoryDB.get_storage().graph
    planet_search_dict = MemoryDB.get_storage().planet_search_dict
    grids = MemoryDB.get_storage().grids
    path_plot = get_shortest_path(graph, planet_search_dict["Coruscant"], planet_search_dict["Jakku"], pairs=True)
    plot_map(graph, path=path_plot, grids=grids)


if __name__ == '__main__':
    manager()
