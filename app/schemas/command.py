from marshmallow import Schema, fields


class MessagePacketSchema(Schema):
    type = fields.String()
    data = fields.String()
    text = fields.String()


class ResponseSchema(Schema):
    role = fields.String()
    action = fields.Boolean()
    target = fields.Boolean()
    message = fields.Nested(MessagePacketSchema, many=True, required=True)
    user = fields.String()


class CommandSchema(Schema):
    # TODO:150 Figure out how to use underscore_case for fields
    # dump_to="newName" works, but it's got all sorts of issues
    id = fields.String()
    name = fields.String(required=True)
    response = fields.String(required=True)
    createdAt = fields.DateTime()
    userLevel = fields.Integer(required=True)
    token = fields.String(required=True)
    response = fields.Nested(ResponseSchema, required=True)
