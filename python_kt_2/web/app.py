from pathlib import Path
from flask import Flask, jsonify, render_template, request
from .. import use_cases

def main():
    app = Flask(__name__)

    @app.get('/')
    def index():
        return jsonify(ping=pong)

    app.run(debug=True)