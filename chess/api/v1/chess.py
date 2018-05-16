# coding=utf-8
from chess.model.exceptions import SongChessError
from chess.utils import Error_jsonify, normal_jsonify
from flask import jsonify, request
from .._bp import create_blueprint
from ..schema.chess import RoomSchema, RecordSchema
from chess.model.chess.chess import Room, Record
from marshmallow.exceptions import MarshmallowError
from chess.api.socket.chess import ChessNamespace

bp = create_blueprint('room', __name__, url_prefix='/room')


chessName = ChessNamespace()

@bp.route('/', methods=['POST'])
def create_and_join_room():
    room_schema = RoomSchema()
    args = room_schema.fill()
    room = Room.add(**args)
    return jsonify(room_schema.dump(room).data)


@bp.route('/<int:room_id>', methods=['GET'])
def get_room_by_id(room_id):
    room_schema = RoomSchema()
    room = Room.get(room_id)
    response = room_schema.dump(room).data
    response.update({'headimgs': room.headimgs})
    return jsonify(response)


@bp.route('/<int:room_id>/members', methods=['PUT'])
def join_room(room_id):
    try:
        room_schema = RoomSchema()
        args = room_schema.fill()

        # 因为设置members是json类型的，传过来的参数是marshmallow会将其转换为json，所以就成str了？先强转下
        room = Room.join_or_leave_room(room_id, int(args.get('members')))

        return jsonify(room_schema.dump(room).data)
    except SongChessError as e:
        return Error_jsonify(data=e.args[0], err_msg=e.message, err_code=e.code)


@bp.route('/<int:room_id>/members/<int:member_id>', methods=['DELETE'])
def leave_room(room_id, member_id):
    try:
        room_schema = RoomSchema()
        room = Room.join_or_leave_room(room_id, member_id, False)
        return jsonify(room_schema.dump(room).data)
    except SongChessError as e:
        return Error_jsonify(data=e.args[0], err_msg=e.message, err_code=e.code)


@bp.route('/<int:room_id>/room_record', methods=['GET', 'POST'])
def get_and_set_record_by_room_id(room_id):
    try:
        record_schema = RecordSchema()
        if request.method == "POST":
            args = record_schema.fill()
            Record.add(room_id, **args)
            # send message to room who are in.
            chessName.on_update_chess_records({'namespace': '/chess', 'room': str(room_id), 'data': 'a new records comes!'})
            return normal_jsonify()
        else:
            record_schema = RecordSchema()
            return jsonify(record_schema.dump(Record.get(room_id)).data)
    except MarshmallowError as e:
        return Error_jsonify(data=e.args[0])

