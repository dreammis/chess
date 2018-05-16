# coding=utf-8
from datetime import datetime
import pickle
import json
from chess.ext import db
from chess.libs.redis import mc, ONE_HOUR
from chess.model.exceptions import UserNotFoundError, RoomNotFoundError, MemberInRoomNotFoundError
from chess.model.user.user import User


class Room(db.Model):
    __tablename__ = 'chess_room'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('chess_user.id'))
    members = db.Column(db.String(64))  # 格式为(1001, 1002) 数字为author_id
    create_time = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship(User, lazy='subquery', backref='room')

    _cache_key_prefix = 'room:'
    _room_cache_key = _cache_key_prefix + 'id:%s'

    def __init__(self, user_id, members=()):
        self.author_id = user_id
        self.members = members

    @staticmethod
    def add(author_id):
        user = User.query.filter_by(id=author_id).first()
        if not user:
            raise UserNotFoundError
        members = [author_id]
        room = Room(user_id=author_id, members=json.dumps(members))
        db.session.add(room)
        db.session.commit()
        return room

    @classmethod
    def get(cls, id_):
        cache_key = cls._room_cache_key % id_
        if mc.get(cache_key):
            return pickle.loads(bytes.fromhex(mc.get(cache_key)))
        room = cls.query.filter_by(id=id_).first()
        # 处理头像
        row = User.query.join('wechat_user').filter(User.id.in_(json.loads(room.members))).with_entities(
            'chess_user.id', 'chess_wechat_user.headimg', 'chess_wechat_user.nickname').all()
        headimgs = [dict(zip(['uid', 'img', 'nickname'], item)) for item in row]
        setattr(room, 'headimgs', headimgs)
        if room:
            mc.set(cache_key, pickle.dumps(room).hex())
            mc.expire(cache_key, ONE_HOUR)
        return room

    @classmethod
    def join_or_leave_room(cls, room_id, member_id, join=True):
        """
        :param room_id:
        :param member_id:
        :param join: join为True则是加入，否则则为leave
        :return:
        """
        room = Room.query.filter_by(id=room_id).first()
        members = json.loads(room.members)
        if member_id not in members and join:
            members.append(member_id)
        elif member_id in members and not join:
            members.remove(member_id)
        else:
            raise MemberInRoomNotFoundError
        room.members = json.dumps(members)
        db.session.add(room)
        db.session.commit()
        cache_key = cls._room_cache_key % room_id
        mc.delete(cache_key)
        return room


class Record(db.Model):
    __tablename__ = 'chess_record'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('chess_room.id'))
    room = db.relationship(Room, lazy='subquery', backref='record')
    records = db.Column(db.Text)  # 格式大致为[{data:{user_id: 1, record:10}, time:timestamp}, ]
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    _cache_key_prefix = 'record:'
    _room_cache_key = _cache_key_prefix + 'room_id:%s'

    @classmethod
    def add(cls, room_id, **kwargs):
        room = Room.query.filter_by(id=room_id).first()
        if not room:
            raise RoomNotFoundError
        kwargs['room'] = room
        record = Record.get(room_id)
        if record:
            records = json.loads(record.records)
            records.append(json.loads(kwargs.get('records')))
            record.records = json.dumps(records)
        else:
            kwargs['records'] = json.dumps([json.loads(kwargs['records'])])
            record = Record(**kwargs)
        db.session.merge(record)
        db.session.commit()
        mc.delete(cls._room_cache_key % room_id)
        return record

    @classmethod
    def get(cls, id_):
        cache_key = cls._room_cache_key % id_
        if mc.get(cache_key):
            return pickle.loads(bytes.fromhex(mc.get(cache_key)))
        room = cls.query.filter_by(room_id=id_).first()
        if room:
            mc.set(cache_key, pickle.dumps(room).hex())
            mc.expire(cache_key, ONE_HOUR)
        return room


