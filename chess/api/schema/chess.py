from marshmallow import fields

from .user import UserSchema

from .base import BaseSchema, FillHelperMixin, ma, JsonField


class RoomSchema(BaseSchema, FillHelperMixin):
    id = fields.Integer(dump_only=True)
    author_id = fields.Integer()
    members = JsonField()
    user = ma.Nested(UserSchema)
    create_time = fields.DateTime("%Y-%m-%d %H:%M:%S", dump_only=True)


class RecordSchema(BaseSchema, FillHelperMixin):
    id = fields.Integer(dump_only=True)
    room = ma.Nested(RoomSchema)
    records = JsonField()
    create_time = fields.DateTime("%Y-%m-%d %H:%M:%S", dump_only=True)
    update_time = fields.DateTime("%Y-%m-%d %H:%M:%S", dump_only=True)
