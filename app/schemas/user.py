from marshmallow import Schema, fields, post_load


class UserSchema(Schema):
    # TODO:150 Figure out how to use underscore_case for fields
    # dump_to="newName" works, but it's got all sorts of issues
    id = fields.String()
    token = fields.String(required=True)
    newCommandId = fields.Integer()
