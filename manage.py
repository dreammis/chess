# -*- coding: utf-8 -*-
from chess.ext import db
from chess.app import create_app
from chess.model.chess.chess import Room, Record
from chess.model.user.user import User, WeChatUser
from config import SongConfig

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from chess.ext import si

# set the mode of async
async_mode = None
  
app = create_app()
manager = Manager(app)  
migrate = Migrate(app, db)
# socketio = SocketIO(app, async_mode=async_mode)
# alchemydumps不支持最新这个版本的flask，暂时去掉
# from flask_alchemydumps import AlchemyDumps, AlchemyDumpsCommand
# alchemydumps = AlchemyDumps(app, db)
# manager.add_command('alchemydumps', AlchemyDumpsCommand)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, Room=Room, Record=Record, User=User, WeChatUser=WeChatUser)

manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def runserver(host=None, port=None, debug=None):
    """Run a flask development server"""
    # app.run(SongConfig.HTTP_HOST, SongConfig.HTTP_PORT, SongConfig.DEBUG)
    # si为socketio启动
    si.run(app, host=SongConfig.HTTP_HOST, port=SongConfig.HTTP_PORT, debug=SongConfig.DEBUG)

@manager.command
def create_db():
    db.create_all()

if __name__ == '__main__':
    manager.run()

