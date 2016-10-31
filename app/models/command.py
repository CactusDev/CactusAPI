import rethinkdb as rethink

from datetime import datetime

import config
from flask_restplus import fields

from remodel.models import Model

from .. import api

utc_now = datetime.utcnow().isoformat()


class Command(Model):

    model = api.model("Command", {
        "name": fields.String(),
        "commandId": fields.Integer(),
        "response": fields.String(),
        "enabled": fields.Boolean(default=True),
        "deleted": fields.Boolean(default=False),
        "userLevel": fields.Integer(default=0),
        "createdAt": fields.DateTime(default=utc_now),
        # "userId": fields.Integer(),
        # "userName": fields.String(),
        "channelName": fields.String(),
        "channelId": fields.Integer()
    })

    def __init__(self, *, name, command_id, response, channel_name, channel_id,
                 created_at=utc_now, enabled=True, deleted=False,
                 user_level=0):
        self.name = name
        self.command_id = command_id
        self.response = response
        # self.user_id = user_id
        # self.user_name = user_name
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.created_at = created_at
        self.enabled = enabled
        self.deleted = deleted
        self.user_level = user_level
