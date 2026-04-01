import os
from flask import Flask, render_template, request, flash, redirect, url_for
from .. import use_cases

app = Flask(__name__)
app.secret_key = "python_kt_2_secret_key"
MAX_FILE_SIZE = 2 * 1024 * 1024 

#главная страничка
@app.route('/')
def index():
    """Отображает стартовую страницу с ссылками на функционал."""
    return render_template('index.html')


#статистика
@app.route('/stats', methods=['GET', 'POST'])
def stats():
    """Анализ количества слов, предложений и символов."""
    results = None
    if request.method == 'POST':
        #проверка наличия файла
        if 'file' not in request.files:
            flash("Ошибка: Файл не выбран", "error")
            return redirect(request.url)
        
        file = request.files['file']
        pos_enabled = 'pos' in request.form 

        if file.filename == '':
            flash("Ошибка: Выберите файл", "error")
            return redirect(request.url)
        
        if not file.filename.lower().endswith('.txt'):
            flash("Ошибка: Разрешены только .txt файлы", "error")
            return redirect(request.url)

        try:
            content = file.read().decode('utf-8')
            results = use_cases.stats(content, pos=pos_enabled)
        except Exception as e:
            flash(f"Ошибка при обработке: {e}", "error")
            return redirect(request.url)

    return render_template('stats.html', results=results)

@app.route('/top', methods=['GET', 'POST'])
def top():
    """Анализ самых частотных слов текста."""
    results = None
    if request.method == 'POST':
        file = request.files.get('file')
        norm_mode = request.form.get('mode', 'stemming')
        if not file or file.filename == '':
            flash("Ошибка: Файл не выбран", "error")
            return redirect(request.url)
        
        if not file.filename.lower().endswith('.txt'):
            flash("Ошибка: Только файлы .txt", "error")
            return redirect(request.url)
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0) 
        
        if file_length > MAX_FILE_SIZE:
            flash(f"Ошибка: Файл слишком большой (макс. {MAX_FILE_SIZE // 1024} КБ)", "error")
            return redirect(request.url)

        try:
            content = file.read().decode('utf-8')
            results = use_cases.top_words(content, normalize_mode=norm_mode)
        except Exception as e:
            flash(f"Ошибка при обработке: {e}", "error")
            return redirect(request.url)

    return render_template('topwords.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)