import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, flash
from .. import use_cases


def main():
    UPLOAD_FOLDER = Path() / "python_kt_2" / "web" / "tmp"
    ALLOWED_EXTENSIONS = {"txt", "md", "log"}

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    @app.get("/")
    def index():
        return render_template("index.html")

    def allowed_file(filename):
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    @app.get("/stats")
    def stats():
        return render_template("stats.html")

    @app.post("/stats")
    def stats_process():
        text_file = request.files.get("file")

        if text_file.filename == "":
            flash("No selected file")
        destination = Path.joinpath(app.config["UPLOAD_FOLDER"], text_file.filename)
        text_file.save(destination)

        text = Path(destination).read_text(encoding="utf-8")
        print(text)

        return jsonify(use_cases.stats(text))

    app.run(debug=True)
