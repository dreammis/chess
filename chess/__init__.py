# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
# from config import config
# from .main import main as main_blueprint
#
#
# db = SQLAlchemy()
# # manager = Manager(chess)
#
#
# def create_app(config_name):
#     app = Flask(__name__)
#     app.config.from_object(config[config_name])
#     config[config_name].init_app(app)
#     db.init_app(app)
#     app.register_blueprint(main_blueprint)
#
# from chess import views
# from ..manage import socketio
#
# __all__ = [
#     'socketio'
# ]
