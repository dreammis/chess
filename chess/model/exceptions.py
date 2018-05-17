from collections import namedtuple
from marshmallow.exceptions import MarshmallowError


Error = namedtuple('Error', ['code', 'message', 'http_status_code'])


class SongChessError(Exception):
    _error = Error(0, '未知错误，请重试', 403)
    sentry_warning = False

    def __init__(self, message=''):
        super(SongChessError, self).__init__(message)
        self.message = message or self._error.message
        self.code = self._error.code
        self.http_status_code = self._error.http_status_code


class ParamInvalidError(MarshmallowError, SongChessError):
    _error = Error(10010, None, 400)


#: 基础类错误(1 ~ 99)
class InvalidValueError(SongChessError):
    _error = Error(1, '请求参数不正确', 400)


class InvalidSMSVerifyCodeError(SongChessError):
    _error = Error(11, '请输入正确的短信验证码', 403)


class InvalidCaptchaError(SongChessError):
    _error = Error(13, '请输入正确的图片验证码', 403)


class EmailFormatError(SongChessError):
    _error = Error(16, 'Email格式错误', 400)


class MobileFormatError(SongChessError):
    _error = Error(17, '手机号格式错误', 400)


class PasswordFormatError(SongChessError):
    _error = Error(18, '请输入6-20位密码，不能包含空格', 400)


class NumberRangeError(SongChessError):
    _error = Error(20, '数字/长度不符合区间要求', 400)


class InvalidDatetimeError(SongChessError):
    _error = Error(21, '日期时间格式错误', 400)


class NameAlreadyExistedError(SongChessError):
    _error = Error(22, '名称重复', 400)


#: 账号类(400~499)
class MobileAlreadyExistedError(SongChessError):
    _error = Error(400, '手机号已存在', 403)


class NameFormatError(SongChessError):
    _error = Error(401, '请正确输⼊姓名，2-10个汉字', 400)


class AliasAlreadyExistedError(SongChessError):
    _error = Error(402, '账号已经存在', 403)


class UserNotFoundError(SongChessError):
    _error = Error(403, '用户不存在', 404)


class RoomNotFoundError(SongChessError):
    _error = Error(403, '该房间不存在', 404)


class RecordNotFoundError(SongChessError):
    _error = Error(403, '该房间记录不存在', 404)


class MemberInRoomNotFoundError(SongChessError):
    _error = Error(403, '该用户在房间记录不存在', 404)


class MemberInRoomAlreadyIn(SongChessError):
    _error = Error(403, '该用户已经在房间中', 404)


class IncorrectPasswordError(SongChessError):
    _error = Error(404, '密码错误', 400)


class EmailAlreadyExistedError(SongChessError):
    _error = Error(405, '邮箱已存在', 403)


class WeixinAlreadyExistedError(SongChessError):
    _error = Error(406, '微信已存在', 403)


class SupplySameAsDemandError(SongChessError):
    _error = Error(407, '供给与需求不可以相同', 403)


class InvalidPostError(SongChessError):
    _error = Error(408, '无效的Post，请重新检查填写的信息', 403)


class DuplicatedPostError(SongChessError):
    _error = Error(409, '重复的Post，请重新检查填写的信息', 403)


class CannotEditPostError(SongChessError):
    _error = Error(410, '修改Post次数已被用完，无法修改', 403)


class CannotViewPostContactError(SongChessError):
    _error = Error(411, '查看联系方式次数已用完，请稍候再试', 403)


class PostNotFoundError(SongChessError):
    _error = Error(412, '此Post不存在', 403)


# 反馈类错误(850~599)
class FeedbackTooLongError(SongChessError):
    _error = Error(850, '描述超过1000字，请重新编辑', 400)


# 请求 limit 之类的错误
class SendSMSTooManyTimesError(SongChessError):
    _error = Error(995, '已超出当日获取验证码最大次数，请24小时后重试', 429)


class LoginTooManyTimesError(SongChessError):
    _error = Error(996, '尝试登陆次数太多', 429)


class AtemptTooManyTimesError(SongChessError):
    _error = Error(997, '尝试次数太多', 429)


class RequestFailedError(SongChessError):
    _error = Error(998, 'Parameters were valid but the request failed.', 402)


class LockError(SongChessError):
    _error = Error(999, '操作太快了！', 429)


class RequestTooFrequentError(SongChessError):
    _error = Error(1000, '您的操作太过频繁，请稍后重试', 429)


class RetryError(SongChessError):
    _error = Error(1500, 'Need retry somehow', 402)


class DownstreamConnectionError(SongChessError):
    _error = Error(1500, 'DownstreamConnectionError', 500)


# 第三方服务异常
class WeChatServiceError(SongChessError):
    _error = Error(4000, 'WeChat Service Error', 403)


class WechatUserNotFoundError(SongChessError):
    _error = Error(4001, 'WeChat User Not Found', 404)


class MissingSessionKeyError(SongChessError):
    _error = Error(4002, 'Missing SessionKey', 401)


class InvalidSessionKeyError(SongChessError):
    _error = Error(4003, 'Invalid SessionKey', 401)


class InvalidMethod(SongChessError):
    _error = Error(4004, 'Invalid Method', 401)
