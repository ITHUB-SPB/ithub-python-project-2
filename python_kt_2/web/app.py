from pathlib import Path
from flask import Flask, jsonify, render_template, request
from .. import use_cases

def main():
    app = Flask(__name__)

    @app.get('/')
    def index():
        return render_template("index.html")

    @app.get("/stats")
    def stats():
        return render_template('stats.html')

    @app.post('/stats')
    def stat_process():
        pos = True if request.form.get('pos') == 'on' else False
        text_file = request.files.get('file')

        destination = Path() / 'python_kt_2' / 'corpus' / text_file.filename
        text_file.save(destination)

        text = destination.read_text(encoding = 'utf-8')

        result =  use_cases.stats(text, pos)
        return  jsonify(result)

    app.run(debug=True)