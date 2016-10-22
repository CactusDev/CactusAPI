from flask_restplus import Resource, fields

model = api.model("Command", {
    "command": fields.String,
    "response": fields.String
})


class CommandResource(Resource):
    @api.marshall_with(CommandModel.model)
    def get(self, **kwargs):
        return CommandModel(command="foo", response="bar")
        # return {"foo": "bar"}

    def post(self):
        return {"spam": "eggs"}


class CommandModel:
    def __init__(self, command, response):
        self.command = command
        self.response = response

        self.status = True


#
# @app.route("/api/v1/channel/<channel>/command", methods=["GET"])
# def user_commands(channel):
#
#     """
#     If you GET this endpoint, simply go to /api/v1/channel/<channel>/command
#     with <channel> replaced for the channel you want to get commands for
#     """
#     model = "Command"
#
#     if channel.isdigit():
#         fields = {"channelId": int(channel), "deleted": False}
#     else:
#         fields = {"channelName": channel.lower(), "deleted": False}
#
#     packet, code = generate_response(
#         model,
#         request.path,
#         request.method,
#         request.values,
#         fields=fields
#     )
#
#     return make_response(jsonify(packet), code)
#
#
# @app.route("/api/v1/channel/<channel>/command/<int:cmd>",
#            methods=["GET", "PATCH", "DELETE"])
# def user_command(channel, cmd):
#     """
#     If you GET this endpoint, go to /api/v1/channel/<channel>/command/<cmd>
#     with <channel> replaced for the channel you want & <cmd> replaced with the
#     command you wish to look up
#
#     If you PATCH this endpoint:
#         Go to /api/v1/channel/<channel>/command/<cmd> with <channel> replaced
#             for the channel wanted & <cmd> replaced with the command you wish
#             to look up or the command ID
#     """
#
#     model = "Command"
#
#     if channel.isdigit():
#         fields = {"channelId": int(channel), "commandId": cmd}
#     else:
#         fields = {"channelName": channel.lower(), "commandId": cmd}
#
#     data = dict(request.values)
#
#     data = {
#         key: request.values.get(key) for key in request.values
#     }
#     data.update(**fields)
#
#     for key in data:
#         if isinstance(data[key], str):
#             data[key] = unescape(data[key])
#
#     data = {key: data[key] for key in data if data[key] is not None}
#
#     response = generate_response(
#         model,
#         request.path,
#         request.method,
#         request.values,
#         data=data,
#         fields=fields
#     )
#
#     packet = response[0]
#
#     return make_response(jsonify(response[0]), response[1])
