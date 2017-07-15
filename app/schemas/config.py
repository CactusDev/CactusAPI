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


class SpamSchema(Schema):
    maxEmoji = fields.Integer(default=6)
    maxCapsScore = fields.Integer(default=16)
    allowUrls = fields.Boolean(default=False)


class BannedPhrasesSchema(Schema):
    response = fields.String(default="")
    action = fields.String(default="none", nullable=True)
    trigger = fields.String(required=True)


class ConfigSchema(Schema):
    id = fields.String()
    token = fields.String(required=True)
    services = fields.Nested(ServiceSchema, many=True)
    announce = fields.Nested(AnnouncementsSchema)
    spam = fields.Nested(SpamSchema)
    whitelistedUrls = fields.List(fields.String)
    bannedPhrases = fields.Nested(BannedPhrasesSchema, many=True)
