from pathlib import Path

from flask import Flask, jsonify, render_template, request

from ..use_cases.stats import stats as stats_use_case

def main():
    app = Flask(__name__)

    @app.get('/')
    def index():
        return jsonify(ping="pong")
    
    @app.get('/stats')
    def test():
        return render_template("stats.html")
    @app.post('/stats')
    def stats_process():
        text_file = request.files.get("text-file")
        pos = bool(request.form.get("pos"))

        destination = Path() / 'python_kt_2' / 'web' / 'media' / text_file.filename
        text_file.save(destination)

        text = destination.read_text(encoding="utf-8")
        result = stats_use_case(text, pos)
        
        return jsonify(result)

    app.run(debug=True)