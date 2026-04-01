import os
import shutil
from pathlib import Path
from flask import Flask, render_template, request, jsonify, flash
from .. import use_cases
from .json2html import json_to_html_table
from markupsafe import Markup


UPLOAD_FOLDER = Path() / "python_kt_2" / "web" / "tmp"
ALLOWED_EXTENSIONS = {"txt", "md", "log"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "sosiska"

shutil.rmtree(UPLOAD_FOLDER)
os.mkdir(UPLOAD_FOLDER)


@app.get("/")
def index():
    return render_template("index.html")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Статистика
@app.get("/stats")
def stats():
    return render_template("stats.html")


@app.post("/stats")
def stats_process():
    text_file = request.files.get("file")
    error = None
    if text_file.filename == "":
        error = "No selected file"
    if not text_file and allowed_file(text_file.filename):
        error = "Invalid filetype"
    if error is not None:
        flash(error)
        return render_template("stats.html", error=error)
    else:
        table = None
        destination = Path.joinpath(app.config["UPLOAD_FOLDER"], text_file.filename)
        text_file.save(destination)
        text = Path(destination).read_text(encoding="utf-8")
        app.logger.debug(text)
        table = Markup(json_to_html_table(use_cases.stats(text)))
        app.logger.debug(table)
        return render_template("stats.html", table=table)


@app.get("/top-words")
def topwords():
    return render_template("top-words.html")


@app.get("/word-cloud")
def wordcloud():
    return render_template("word-cloud.html")


@app.get("/about")
def about():
    return render_template("about.html")


app.run(debug=True)
