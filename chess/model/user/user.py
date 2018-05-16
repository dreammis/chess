import pickle
from datetime import datetime

from chess.ext import db
from chess.libs.redis import mc, ONE_DAY, ONE_HOUR
from chess.model.exceptions import (WechatUserNotFoundError)


class User(db.Model):
    __tablename__ = 'chess_user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), index=True)
    create_time = db.Column(db.DateTime(), default=datetime.now())

    __mapper_args__ = {
        'polymorphic_identity': 'user'
    }

    _cache_key_prefix = 'student:'
    _student_cache_key = _cache_key_prefix + 'id:%s'

    def __init__(self, username):
        self.username = username

    @staticmethod
    def add(username):
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return user.id

    @classmethod
    def get(cls, id_):
        cache_key = cls._student_cache_key % id_
        if mc.get(cache_key):
            return pickle.loads(bytes.fromhex(mc.get(cache_key)))
        student = cls.query.filter_by(id=id_).first()
        if student:
            mc.set(cache_key, pickle.dumps(student).hex())
            mc.expire(cache_key, ONE_HOUR)
        return student


class WeChatUser(db.Model):
    __tablename__ = 'chess_wechat_user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    openid = db.Column(db.String(30), unique=True, index=True)
    nickname = db.Column(db.String(64))
    headimg = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('chess_user.id'))
    user = db.relationship(User, lazy='subquery', backref='wechat_user', uselist=False)
    session_key = db.Column(db.String(80), unique=True)

    # third_session_key 目前业务不需要自定义session_key以及expire_time

    _cache_key_prefix = 'wechat_user:'
    _wechat_user_by_open_id_cache_key = _cache_key_prefix + 'open_id:%s'

    @staticmethod
    def get_by_open_id(open_id):
        cache_key = WeChatUser._wechat_user_by_open_id_cache_key % open_id
        if mc.get(cache_key):
            return pickle.loads(bytes.fromhex(mc.get(cache_key)))
        wechat_user = WeChatUser.query.filter_by(openid=open_id).first()
        if wechat_user:
            mc.set(cache_key, pickle.dumps(wechat_user).hex())
            mc.expire(cache_key, ONE_DAY)
        else:
            raise WechatUserNotFoundError
        return wechat_user

    @staticmethod
    def add(**kwargs):
        username = kwargs.get('openid')
        wechat_user = WeChatUser.query.filter_by(openid=username).first()
        if not wechat_user:
            user = User(username)
            kwargs['user'] = user
            wechat_user = WeChatUser(**kwargs)
            db.session.add_all([user, wechat_user])
            db.session.commit()
        return wechat_user


