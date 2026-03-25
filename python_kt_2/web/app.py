from pathlib import Path
from flask import Flask, render_template, request, jsonify
from .. import use_cases


def main():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/stats")
    def stats():
        return render_template("stats.html")

    @app.post("/stats")
    def stats_process():
        text_file = request.files.get("file")
        destination = Path() / "python_kt_2" / "web" / "tmp" / text_file.filename
        text_file.save(destination)

        text = Path(destination).read_text(encoding="utf-8")
        print(text)

        return jsonify(use_cases.stats(text))

    app.run(debug=True)
