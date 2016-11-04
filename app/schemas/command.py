from marshmallow import Schema, fields, post_load

from datetime import datetime


class CommandSchema(Schema):
    # TODO: Figure out how to use underscore_case for fields
    # Should be dump_to="newName", but it's not working :/
    id = fields.String()
    name = fields.String(required=True)
    response = fields.String(required=True)
    commandId = fields.Integer()
    createdAt = fields.DateTime()
    enabled = fields.Bool()
    deleted = fields.Bool()
    userLevel = fields.Integer(required=True)
    token = fields.String(required=True)
