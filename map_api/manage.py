from app.main import flask_app
from flask_script import Manager
from app.graph_functions.graph_factory import build_and_plot_test_graph


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
    build_and_plot_test_graph()


if __name__ == '__main__':
    manager.run()
