class UserResource:
    pass


@app.route("/api/v1/user/<string:username>",
           methods=["GET", "PATCH", "DELETE"])
def beam_user(username):

    """
    If you GET this endpoint, simply go to /api/v1/user/<username> with
    <username> replaced for the user you want

    If you PATCH this endpoint:
        Go to /api/v1/user/<username> with <username> replaced for the user
            wanted
        Parameters needed:
            - email:    User's email address
            - provider: OAuth provider
            - pid:      User ID from OAuth provider
    """
    model = "User"

    fields = {"channelId": channel,
              "quoteId": quote}

    data = {
        "email": request.values.get("email"),
        "providerId": "{}${}".format(request.values.get("provider", ""),
                                     request.values.get("pid", "")),
        "roles": ["user"],
        "userName": username
    }

    for key in data:
        if isinstance(data[key], str):
            data[key] = unescape(data[key])

    data = {key: data[key] for key in data if data[key] is not None}

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
