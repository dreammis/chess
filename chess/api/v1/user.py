from chess.utils import normal_jsonify, Error_jsonify
from flask import jsonify
from .._bp import create_blueprint
from ..schema.user import UserSchema, WeChatUserSchema
from chess.model.user.user import User, WeChatUser
from marshmallow.exceptions import MarshmallowError

bp = create_blueprint('user', __name__, url_prefix='/user')


@bp.route('/', methods=['POST'])
def add_user():
    args = UserSchema().fill()
    user = User.add(**args)
    return jsonify(user)


@bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user_schema = UserSchema()
    return jsonify(user_schema.dump(User.get(user_id)).data)


@bp.route('/wechat/<string:openid>', methods=['GET'])
def get_wechat_user(openid):
    try:
        user_schema = WeChatUserSchema()
        data = user_schema.dump(WeChatUser.get_by_open_id(openid)).data
    except Exception as e:
        return normal_jsonify(err_code=e.code, err_msg=e.message, status_code=e.http_status_code)
    return jsonify(data)


@bp.route('/wechat/', methods=['POST'])
def add_wechat_user():
    try:
        args = WeChatUserSchema().fill()
        user = WeChatUser.add(**args)
        return jsonify(WeChatUserSchema().dump(user).data)
    except MarshmallowError as e:
        return Error_jsonify(data=e.args[0])

