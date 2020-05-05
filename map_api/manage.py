from app.main import flask_app
from flask_script import Manager
from app.main.local_graph_storage import MemoryDB
from app.graph_functions.graph_factory import get_shortest_path, plot_map


flask_app.app_context().push()

manager = Manager(flask_app)


@manager.command
def run():
    flask_app.run()


@manager.command
def migrateup():
    pass


@manager.command
def plotgraph():
    graph = MemoryDB.get_storage().graph
    planet_search_dict = MemoryDB.get_storage().planet_search_dict
    grids = MemoryDB.get_storage().grids
    path_plot = get_shortest_path(graph, planet_search_dict["Coruscant"], planet_search_dict["Jakku"], pairs=True)
    plot_map(graph, path=path_plot, grids=grids)


if __name__ == '__main__':
    manager.run()
