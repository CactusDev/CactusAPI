from marshmallow import Schema, fields


class CommandSchema(Schema):
    # TODO:150 Figure out how to use underscore_case for fields
    # dump_to="newName" works, but it's got all sorts of issues
    id = fields.String()
    name = fields.String(required=True)
    response = fields.String(required=True)
    commandId = fields.Integer()
    createdAt = fields.DateTime()
    enabled = fields.Bool()
    deleted = fields.Bool()
    userLevel = fields.Integer(required=True)
    token = fields.String(required=True)
