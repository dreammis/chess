from marshmallow import fields
from marshmallow import validate

from .base import BaseSchema, FillHelperMixin, ma


class UserSchema(BaseSchema, FillHelperMixin):
    id = fields.Integer(dump_only=True)
    username = fields.Str()
    create_time = fields.DateTime("%Y-%m-%d %H:%M:%S")


class WeChatUserSchema(BaseSchema, FillHelperMixin):
    openid = fields.Str(validate=validate.Length(max=30), required=True)
    nickname = fields.Str(validate=validate.Length(max=64), required=True)
    headimg = fields.Str(validate=validate.Length(max=200), required=True)
    session_key = fields.Str(validate=validate.Length(max=80))
    user = ma.Nested(UserSchema)
