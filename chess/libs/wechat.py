from chess.libs.redis import mc
import requests

from chess.model.exceptions import WeChatServiceError
from flask import json, make_response
from ..app import SongConfig


class WeChat(object):

    JSCODE2SESSION_URL = 'https://api.weixin.qq.com/sns/jscode2session'
    GET_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'
    GET_APP_QRCOODE_URL = 'https://api.weixin.qq.com/wxa/getwxacode?access_token={access_token}'

    _wechat_access_token_cache_key = "wechat_key"

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    @property
    def access_token(self):
        access_token_cache = mc.get(self._wechat_access_token_cache_key)
        if not access_token_cache:
            access_token = self.get_access_token()
            if access_token:
                mc.set(self._wechat_access_token_cache_key, access_token, 6600)
                return access_token
            else:
                return None
        else:
            return access_token_cache

    def jscode2session(self, code, grant_type='authorization_code'):
        params = dict(appid=self.app_id, secret=self.app_secret,
                      js_code=code, grant_type=grant_type)
        return json.loads(requests.get(self.JSCODE2SESSION_URL, params=params).text)

    def get_access_token(self, grant_type='client_credential'):
        params = dict(appid=self.app_id, secret=self.app_secret, grant_type=grant_type)
        r = requests.get(self.GET_ACCESS_TOKEN_URL, params=params)
        if r.status_code == 200:
            access_token = r.json().get('access_token')
            return access_token
        raise WeChatServiceError()

    def get_app_qrcode_by_path(self, path):
        json = dict(path=path)
        url = self.GET_APP_QRCOODE_URL.format(access_token=self.access_token)
        r = requests.post(url, json=json)
        res = make_response(r.content)
        res.headers['Content-Type'] = r.headers['Content-Type']
        return res

wechat = WeChat(SongConfig.WEIXIN_APP_ID, SongConfig.WEIXIN_APP_SECRET)


