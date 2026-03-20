from flask import Flask, jsonify


def main():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return jsonify(ping="pong")

    app.run(debug=True)