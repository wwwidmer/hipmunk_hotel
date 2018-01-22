from flask import Flask
app = Flask(__name__)

from hotels.main import hotel_blueprint

app.register_blueprint(hotel_blueprint)


@app.route("/")
def index():
    return 'List of all API urls'

if __name__ == '__main__':
    app.run(port=8000)
