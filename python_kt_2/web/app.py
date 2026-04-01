import os
from flask import Flask, render_template, request, flash, redirect, url_for
from ..use_cases.stats import execute as run_stats_logic
from ..use_cases.word_cloud import execute as run_cloud_logic

app = Flask(__name__)
app.secret_key = "super_secret_key_kt2"

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    data = None
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not allowed_file(file.filename):
            flash("Ошибка: Загрузите файл формата .txt")
            return redirect(request.url)
        
        try:
            text = file.read().decode('utf-8')
            pos_mode = 'pos' in request.form
            data = run_stats_logic(text, pos_mode)
        except Exception as e:
            flash(f"Ошибка при чтении файла: {e}")
            return redirect(request.url)
        
    return render_template('stats.html', result=data)

@app.route('/cloud', methods=['GET', 'POST'])
def cloud():
    img_data = None
    if request.method == 'POST':
        file = request.files.get('file')
        
        if not file or not allowed_file(file.filename):
            flash("Ошибка: Неверный формат файла")
            return redirect(request.url)
            
        file_content = file.read()
        if len(file_content) > 2097152:
            flash("Ошибка: Файл слишком большой (макс. 2МБ)")
            return redirect(request.url)

        try:
            text = file_content.decode('utf-8')
            mode = request.form.get('mode', 'base')
            img_data = run_cloud_logic(text, mode)
        except Exception as e:
            flash(f"Ошибка генерации: {e}")
            return redirect(request.url)
        
    return render_template('cloud.html', image=img_data)

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()

