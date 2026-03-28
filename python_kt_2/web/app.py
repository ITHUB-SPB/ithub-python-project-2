from collections.abc import Iterable
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request
from werkzeug.datastructures import FileStorage

from python_kt_2.core.preprocess import preprocess_text
from python_kt_2.use_cases.top_words import (
    count_words,
    lemmatization_text,
    stemming_text,
)

from ..use_cases.stats import stats as stats_use_case


def main():
    app = Flask(__name__)
    app.secret_key = "dog"

    @app.get("/")
    def index():
        return render_template("main.html")

    @app.get("/stats")
    def test():
        return render_template("stats.html")

    @app.post("/stats")
    def stats_process():
        text_file = request.files.get("text")

        if not text_file:
            flash("Где файл, собака?")
            return redirect("/stats")

        pos = request.form.get("pos") == "on"

        destination = Path() / "python_kt_2" / "web" / "media" / text_file.filename
        text_file.save(destination)

        if text_file.filename[-4:] != ".txt":
            flash(
                "Неверный формат файла. Пожалуйста, загрузите текстовый файл с расширением .txt"
            )
            return redirect("/stats")

        text = destination.read_text(encoding="utf-8")
        result = stats_use_case(text, pos)

        return render_template("stats_result.html", result=result)

    @app.get("/top")
    def dog():
        return render_template("top.html")

    @app.post("/top")
    def cat():
        text_file = request.files.get("text")

        if not text_file:
            flash("Где файл, собака?")
            return redirect("/stats")

        normalization_type = request.form.get("normalization")
        destination = Path() / "python_kt_2" / "web" / "media" / text_file.filename
        text_file.save(destination)

        if text_file.filename[-4:] != ".txt":
            flash(
                "Неверный формат файла. Пожалуйста, загрузите текстовый файл с расширением .txt"
            )
            return redirect("/top")

        text = destination.read_text(encoding="utf-8")
        text = preprocess_text(text)

        result: Iterable[str] = []
        match normalization_type:
            case "Лемматизация":
                result = lemmatization_text(text)
            case "Стемминг":
                result = stemming_text(text)

        result = count_words(result)

        return render_template("top_result.html", result=result)

    app.run(debug=True)
