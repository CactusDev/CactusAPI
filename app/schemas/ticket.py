from marshmallow import Schema, fields, post_load


class CommandSchema(Schema):
    # TODO:150 Figure out how to use underscore_case for fields
    # dump_to="newName" works, but it's got all sorts of issues
    id = fields.String()
    title = fields.String(required=True)
    contents = fields.String(required=True)
    flags = fields.Integer(required=True)
    mentions = fields.List(required=True)
    createdAt = fields.DateTime()
