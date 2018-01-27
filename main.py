from flask import Flask, url_for, jsonify

app = Flask(__name__)

from hotels.main import hotel_blueprint

app.register_blueprint(hotel_blueprint)


@app.route("/")
def index():
    api_endpoints = {}
    for rule in app.url_map.iter_rules():
        if len(rule.defaults or ()) >= len(rule.arguments or ()):
            api_endpoints[rule.endpoint] = url_for(rule.endpoint)
    return jsonify(api_endpoints)

if __name__ == '__main__':
    app.run(port=8000)
