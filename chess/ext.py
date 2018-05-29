# coding=utf-8

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO

db = SQLAlchemy()
ma = Marshmallow()
si = SocketIO(async_mode="eventlet")


# START 这里是Sentry对flask的支持，暂时不需要
# from chess.config import SENTRY_DSN
# import logging
#
# sentry = Sentry(logging=True, level=logging.ERROR, dsn=SENTRY_DSN)
# END


