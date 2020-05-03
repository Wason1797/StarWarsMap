from ..settings import Config


def create_app(config_class):
    from flask import Flask
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)
    return flask_app


def register_blueprints(flask_app):
    from .service import urls
    flask_app.register_blueprint(urls, url_prefix='/')


def register_plugins(flask_app):
    pass


def start_storage():
    from .local_graph_storage import MemoryDB
    MemoryDB.init_storage()


def cors_app(flask_app):
    from flask_cors import CORS
    CORS(flask_app)


def configure_app(config_class):
    flask_app = create_app(config_class)
    register_blueprints(flask_app)
    register_plugins(flask_app)
    cors_app(flask_app)
    start_storage()

    return flask_app


flask_app = configure_app(Config)
