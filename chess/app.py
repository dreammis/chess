import sys

from flask import Flask
from werkzeug.utils import import_string

sys.path.append('../')
from config import SongConfig

extensions = [
    'chess.ext:db',
    'chess.ext:ma',
    'chess.ext:si'
]

blueprints = [
    'chess.api.v1.user.bp',
    'chess.api.v1.chess.bp',
    'chess.api.v1.wechat.bp',
    'chess.api.socket.chess.bp'
]
# socketio = SocketIO()


def create_app(config=None):
    app = Flask(__name__)
    # app.config.from_object('envcfg.json.black_market')
    app.config.from_object(SongConfig)
    app.config.from_object(config)
    for ext_name in extensions:
        extension = import_string(ext_name)
        extension.init_app(app)

    for blueprint_name in blueprints:
        blueprint = import_string(blueprint_name)
        app.register_blueprint(blueprint)

    # socketio.init_app(app)

    return app
