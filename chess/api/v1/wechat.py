from chess.api.schema.user import WeChatUserSchema
from chess.utils import Error_jsonify
from flask import request, jsonify

from .._bp import create_blueprint
from chess.model.user.user import WeChatUser
from ...libs.wechat import wechat
from marshmallow.exceptions import MarshmallowError

bp = create_blueprint('wechat', __name__, url_prefix='/wechat')


@bp.route('/', methods=['GET'])
def get_wechat_openid():
    try:
        js_code = request.args.get('js_code')
        content = wechat.jscode2session(js_code)
        if not content.get('errcode'):
            wechat_schema = WeChatUserSchema()
            args = wechat_schema.fill(extra={'openid': content['openid'], 'session_key': content['session_key']})
            wechat_user = WeChatUser.add(**args)
            content.update(wechat_schema.dump(wechat_user).data)
        return jsonify(content)
    except MarshmallowError as e:
        return Error_jsonify(data=e.args[0])


@bp.route('/qrcode/', methods=['GET'])
def get_wxcode():
    path = request.args.get('path')
    content = wechat.get_app_qrcode_by_path(path)
    return content



