# from envcfg.json.song import DEBUG
# from envcfg.json.song import HTTP_HOST
# from envcfg.json.song import HTTP_PORT
# from envcfg.json.song import DOMAIN
# from envcfg.json.song import SECRET_KEY
# from envcfg.json.song import SQLALCHEMY_DATABASE_URI
# from envcfg.json.song import SQLALCHEMY_ECHO
# from envcfg.json.song import REDIS_DSN
# from envcfg.json.song import WEIXIN_APP_ID
# from envcfg.json.song import WEIXIN_APP_SECRET
# from envcfg.json.song import CELERY_BROKER_URL
# from envcfg.json.song import CELERY_RESULT_BACKEND
import os

from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

APP = 'song'

class SongConfig:
    DEBUG = True if os.getenv("SONG_DEBUG") == 'True' else False
    HTTP_HOST = os.getenv("SONG_HTTP_HOST")
    HTTP_PORT = os.getenv("SONG_HTTP_PORT")
    DOMAIN = os.getenv("SONG_DOMAIN")
    SECRET_KEY = os.getenv("SONG_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SONG_SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = True if os.getenv("SONG_SQLALCHEMY_ECHO") == 'True' else False
    REDIS_DSN = os.getenv("SONG_REDIS_DSN")
    WEIXIN_APP_ID = os.getenv("SONG_WEIXIN_APP_ID")
    WEIXIN_APP_SECRET = os.getenv("SONG_WEIXIN_APP_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = True if os.getenv("SONG_SQLALCHEMY_TRACK_MODIFICATIONS") == 'True' else False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True if os.getenv("SONG_SQLALCHEMY_COMMIT_ON_TEARDOWN") == 'True' else False






    #DATABASE_URI = 'mysql://root:aA123456@localhost/song?charset=utf8mb4'

__all__ = [
    'DEBUG',
    'HTTP_HOST',
    'HTTP_PORT',
    'DOMAIN',
    'SECRET_KEY',
    'SQLALCHEMY_DATABASE_URI',
    'SQLALCHEMY_ECHO',
    'REDIS_DSN',
    'WEIXIN_APP_ID',
    'WEIXIN_APP_SECRET',
    'SQLALCHEMY_TRACK_MODIFICATIONS',
    'SQLALCHEMY_COMMIT_ON_TEARDOWN',
]
