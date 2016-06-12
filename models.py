from run import db


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String)
    userLevel = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, default=True)
    botUsername = db.Column(db.String)
    botPassword = db.Column(db.String)


class Roles(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    channelId = db.Column(db.String)
    userId = db.Column(db.String)
    userLevel = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime)


class Channels(db.Model):
    __tablename__ = "channels"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.String)
    enabled = db.Column(db.Boolean, default=True)
    createdAt = db.Column(db.DateTime)
    service = db.Column(db.String)


class Configuration(db.Model):
    __tablename__ = "configuration"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    channelId = db.Column(db.String)
    key = db.Column(db.String)
    value = db.Column(db.String)
    lastUpdated = db.Column(db.DateTime)


class Commands(db.Model):
    __tablename__ = "commands"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    response = db.Column(db.String)
    enabled = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)
    channelId = db.Column(db.String)
    userLevel = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime)
    userId = db.Column(db.String)
    syntax = db.Column(db.String)
    help = db.Column(db.String)
    builtIn = db.Column(db.Boolean, default=False)


class Messages(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    channelId = db.Column(db.String)
    userId = db.Column(db.String)
    createdAt = db.Column(db.DateTime)


class Executions(db.Model):
    __tablename__ = "executions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commandId = db.Column(db.String)
    messageId = db.Column(db.String)


class Quotes(db.Model):
    __tablename__ = "quotes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quoteId = db.Column(db.Integer)
    messageId = db.Column(db.String)
    channelId = db.Column(db.String)
    userId = db.Column(db.String)
    createdAt = db.Column(db.DateTime)
    enabled = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)
