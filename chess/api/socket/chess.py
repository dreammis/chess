from chess.ext import si as socketio
from chess.api.socket import bp
from chess.model.socket.chess import ChessNamespace

__all__ = [
    'bp'
]

socketio.on_namespace(ChessNamespace('/chess'))
#
#
# @socketio.on('my_ping', namespace='/test')
# def ping_pong():
#     emit('my_pong')
#
#
# @socketio.on('connect', namespace='/test')
# def test_connect():
#     emit('my_response', {'data': 'Connected', 'count': 0})
#
#
# @socketio.on('my_event', namespace='/test')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']})
#
#
# @socketio.on('join', namespace='/test')
# def join(message):
#     join_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'In rooms: ' + ', '.join(rooms()),
#           'count': session['receive_count']})
#
#
# @socketio.on('my_room_event', namespace='/test')
# def send_room_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          room=message['room'])
