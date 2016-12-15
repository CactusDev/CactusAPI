from dateutil import parser
from marshmallow import Schema, fields

from ..util import helpers


class ServiceSchema(Schema):
    name = fields.String(required=True)
    isOAuth = fields.Boolean(default=False, required=True)
    username = fields.String()
    password = fields.String()
    permissions = fields.List(fields.String())


class Announcement(Schema):
    announce = fields.Boolean(default=False)
    message = fields.String()


class AnnouncementsSchema(Schema):
    join = fields.Nested(Announcement)
    follow = fields.Nested(Announcement)
    leave = fields.Nested(Announcement)
    sub = fields.Nested(Announcement)
    host = fields.Nested(Announcement)


class ModNotifier(Schema):
    notify = fields.Boolean(default=False, required=True)
    userNames = fields.List(fields.String, required=True)


class SpamSchema(Schema):
    maxEmoji = fields.Integer()
    autoTimeout = fields.Boolean(default=False)
    notifyMod = fields.Nested(ModNotifier)
    allowLinks = fields.Boolean(default=True)


class ConfigSchema(Schema):
    id = fields.String()
    token = fields.String(required=True)
    services = fields.Nested(ServiceSchema, many=True)
    announce = fields.Nested(AnnouncementsSchema)
    spam = fields.Nested(SpamSchema)
