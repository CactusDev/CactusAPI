from flask import Flask, request, jsonify

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")


@app.route("/test", methods=["POST", "PATCH", "GET"])
def test():
    args = request.args
    json = request.get_json()
    print("args:\t", args)
    print("json:\t", json)
    if json is None:
        data = {"args": args}
    else:
        data = {"args": args, "json": json}
    return jsonify(data)

app.run(port=8000)
