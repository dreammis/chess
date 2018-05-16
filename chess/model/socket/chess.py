from flask_socketio import Namespace, emit, join_room, leave_room


class ChessNamespace(Namespace):

    def on_join_chess_room(self, kwargs):
        join_room(kwargs['room'])
        emit('chess_join', {'data': 'Some one has joined the room'}, room=kwargs['room'])

    def on_leave_chess_room(self, kwargs):
        leave_room(kwargs['room'])
        emit('chess_leave', {'data': 'Some one has left the room'}, room=kwargs['room'])

    def on_update_chess_records(self, kwargs):
        emit('chess_records_update', {'data': kwargs['data']}, **kwargs)

    #
    # def on_join(self, message):
    #     """
    #     :param message: {"room": "roomname", "uid": uid111}
    #     :return:
    #     """
    #     # join_room(**kwargs)
    #     # kwargs.pop('room')
    #     # emit('join_status', {'data': 'In rooms: ' + ', '.join(rooms(**kwargs)), \
    # 'sid': kwargs['sid']}, namespace='/chess')
    #     join_room(message['room'])
    #     emit('join_status',
    #          {'data': 'In rooms: ' + ', '.join(rooms())})
    #
    # def on_mama(self, message):
    #     print('Client disconnected', request.sid)
    #
    # def on_leave(self, message):
    #     leave_room(message['room'])
    #     emit('my_response',
    #          {'data': 'In rooms: ' + ', '.join(rooms())})
    #
    # def on_close_room(self, message):
    #     emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.'},
    #          room=message['room'])
    #     close_room(message['room'])
    #
    # # def on_my_room_event(self, message):
    # #     emit('my_response', {'data': message['data']}, room=message['room'])
    #
    # def on_my_room_event(self, kwargs):
    #     emit('room_message_event', {'data': kwargs['data'], 'uid': kwargs['uid']}, **kwargs)
    #
    # def on_disconnect_request(self):
    #     session['receive_count'] = session.get('receive_count', 0) + 1
    #     emit('my_response',
    #          {'data': 'Disconnected!', 'count': session['receive_count']})
    #     disconnect()
    #
    # def on_my_ping(self):
    #     emit('my_pong')
    #     self.on_my_room_event({"room":"qqq","data":"zzzzzzzz"})
    #
    # def on_connect(self):
    #     emit('my_response', {'data': 'Connected', 'count': 0})
    #
    # def on_disconnect(self):
    #     print('Client disconnected', request.sid)

