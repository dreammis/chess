# chess
WeChat miniprogram for the chess room

chess recorder can record the score of the mahjong or cards game.

Simple introduction of the project

1. .env is the mainly configuration of the project
    such as: HOST, PORT, DATABASE..etc
2.  chess/app is the route of the project which will read the config, register the blueprint and extend the extension.
    ext is the define of the SQLAlchemy, Marshallow and the SocketIO
3.  models
    chess model include the room and record model
    user model include the user and wechat user model
    socket model include the websocket function which inherit the SocketIO
4.  libs
   define the redis server and the wechat functions
5.  api
    schema use the Marshallow to validate the params and serialize and deserialize the data.
    
I use django on my work, first use the flask on the production

Thanks to the @wangzhihao1995, learn a lot from his Repositories [PyBlackMarket](https://github.com/wangzhihao1995/PyBlackMarket)