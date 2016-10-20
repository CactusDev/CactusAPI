
@app.route("/api/v1/channel/<channel>/message", methods=["GET"])
def chan_messages(channel):

    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/messages
    with <channel> replaced for the messages you want to get
    """

    model = "Message"

    if channel.isdigit():
        fields = {"channelId": int(channel)}
    else:
        fields = {"owner": channel.lower()}

    packet, code = generate_response(
        model,
        request.path,
        request.method,
        request.values,
        fields=fields
    )

    return make_response(jsonify(packet), code)


@app.route("/api/v1/channel/<channel>/message/<message>",
           methods=["GET", "POST", "DELETE"])
def chan_message(channel, message):
    """
    If you GET this endpoint, go to /api/v1/channel/<channel>/message/<message>
    with <channel> replaced for the channel you want and <message> for the
    the message ID you want to look up. Will return the raw packet for the
    message as well, unlike /channel/<channel>/message

    If you POST this endpoint:
        Go to /api/v1/channel/<channel>/message/<message> with <channel>
        for the channel wanted & <message> replaced for the ID of the message
        you want to edit or create

        Parameters:
            - message:      Raw message contents in string
            - timestamp:    A Unix-epoch int of when the message was sent
            - userId:       The user ID who sent the message
            - packet:       The raw JSON packet in string form from Beam
    """

    model = "Message"
    errors = []

    required_parameters = ["message", "timestamp", "userId", "packet"]

    for param in request.values:
        if param not in required_parameters:
            errors.append(
                generate_error(
                    uid=uuid4(),
                    status="400",
                    title="Incorrect parameters for endpoint",
                    detail="Missing required {} parameter".format(param),
                    source={"pointer": request.path}
                )
            )

    channel = int(channel) if channel.isdigit() else channel

    fields = {"channelId": channel, "messageId": message}

    data = {
        key: request.values.get(key) for key in request.values
    }
    data.update(**fields)
    data.update({
        "createdAt": rethink.epoch_time(
            int(request.values.get("timestamp", time.time()))
        )
    })

    data = {key: unescape(data[key]) for key in data
            if isinstance(data[key], str)}

    response = generate_response(
        model,
        request.path,
        request.method,
        request.values,
        data=data,
        fields=fields
    )

    packet = response[0]

    return make_response(jsonify(response[0]), response[1])
