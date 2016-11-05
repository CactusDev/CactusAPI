fields = {
    "quoteId": {
        "type": int
    },
    "messageId": {
        "type": str
    },
    "channelId": {
        "type": str
    },
    "channelName": {
        "type": str
    },
    "userId": {
        "type": str
    },
    "quote": {
        "type": str
    },
    "createdAt": {
        "type": datetime,
        "default": rethink.now().run(rethink.connect(
            db=config.RDB_DB,
            port=config.RDB_PORT,
            host=config.RDB_HOST
        ))
    },
    "enabled": {
        "type": bool,
        "default": True
    },
    "deleted": {
        "type": bool,
        "default": False
    }
}
