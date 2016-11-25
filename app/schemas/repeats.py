from marshmallow import Schema, fields


class RepeatSchema(Schema):
    # TODO:150 Figure out how to use underscore_case for fields
    # dump_to="newName" works, but it's got all sorts of issues
    id = fields.String()
    text = fields.String(required=True)
    period = fields.Integer(required=True, default=900)
    token = fields.String(required=True)
    repeatId = fields.Integer(required=True)
