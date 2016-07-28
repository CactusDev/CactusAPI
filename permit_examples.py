@APP.route("/api/v1/channel/<int:channel>/permit/<int:user>",
           methods=["GET", "PATCH", "DELETE"])
def chan_permit(channel, user):
    """
    This endpoint is used to check and set permits on a per-channel, per-user
    basis.

    Methods:
        - GET:
            This method will return the information about a
    """

    redis_key = "{}${}".format(channel, user)

    if request.method == "GET":
        if not REDIS_CONN.exists(redis_key):
            # That individual permit does not exist, return a "succes"
            return make_response(jsonify(None), 204)
        else:
            return make_response(
                jsonify(
                    {
                        "permitted": True,
                        "remaining": REDIS_CONN.ttl(redis_key),
                        "userId": user
                    }
                ), 200
            )

    elif request.method == "PATCH":
        expires_at = request.values.get("expires", None)
        if expires_at is None or int(expires_at) < 5:
            """
            Return 406 error, the expires parameter is REQUIRED when PATCH-ing
            No infinite permits, should friend the user instead
            Permit period must be longer than 5 seconds
            """
            # TODO: Return an error explaining should friend the user
            return make_response(jsonify(None), 406)

        # If it's None, then the channel doesn't exist, we'll need to add it
        if not REDIS_CONN.exists(redis_key):
            # TODO: Add error catching on redis return code
            REDIS_CONN.setex(redis_key, True, expires_at)

            return make_response(
                jsonify(
                    {
                        "permitted": True,
                        "remaining": REDIS_CONN.ttl(redis_key),
                        "userId": user
                    }
                ), 200
            )
        else:
            # Key does exist, let's update the permit expiration
            REDIS_CONN.setex(redis_key, True, expires_at)

            return make_response(
                jsonify(
                    {
                        "permitted": True,
                        "remaining": REDIS_CONN.ttl(redis_key),
                        "userId": user
                    }
                ), 200
            )

    elif request.method == "DELETE":
        # Check if the key even exists
        if REDIS_CONN.exists(redis_key):
            # It does, let's continue
            # TODO: Redis error catching
            REDIS_CONN.delete(redis_key)

            return make_response(jsonify(None), 200)
        else:
            # Key doesn't exist, can't delete it, return successful error
            return make_response(jsonify(None), 204)
