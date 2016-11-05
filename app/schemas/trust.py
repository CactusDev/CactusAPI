from marshmallow import Schema, fields


class TrustSchema(Schema):
    # TODO:150 Figure out how to use underscore_case for fields
    # dump_to="newName" works, but it's got all sorts of issues
    id = fields.String()
    userName = fields.String(required=True)
    userId = fields.String(required=True)
    active = fields.Boolean()
    token = fields.String(required=True)
