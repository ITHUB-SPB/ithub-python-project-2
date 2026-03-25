from flask import Flask, render_template


def main():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/stats")
    def stats():
        return render_template("stats.html")

    app.run(debug=True, port=5001)
