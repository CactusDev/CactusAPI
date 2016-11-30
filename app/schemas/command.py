from marshmallow import Schema, fields


class MessagePacketSchema(Schema):
    type = fields.String(required=True)
    data = fields.String(required=True)
    text = fields.String(required=True)


class ResponseSchema(Schema):
    message = fields.Nested(MessagePacketSchema, many=True, required=True)
    user = fields.String()
    role = fields.Integer()
    action = fields.Boolean()
    target = fields.String(allow_none=True)


class CommandSchema(Schema):
    # TODO: 150 Figure out how to use underscore_case for fields
    # dump_to="newName" works, but it's got all sorts of issues
    id = fields.String()
    name = fields.String(required=True)
    response = fields.Nested(ResponseSchema, required=True)
    createdAt = fields.DateTime()
    token = fields.String(required=True)
    userLevel = fields.Integer(required=True)