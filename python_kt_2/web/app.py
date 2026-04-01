from pathlib import Path
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from .. import use_cases
import os

app = Flask(__name__, template_folder='templates', static_folder='static')


UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  \

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/stats')
def stats_page():
    return render_template('stats.html')

@app.post('/stats')
def stats_upload():
    try:
        \
        if 'file' not in request.files:
            return render_template('stats.html', error='Пожалуйста, выберите файл'), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('stats.html', error='Пожалуйста, выберите файл'), 400
        
        if not allowed_file(file.filename):
            return render_template('stats.html', error='Допускаются только текстовые файлы (.txt)'), 400
        
        
        content = file.read().decode('utf-8', errors='ignore')
        
       
        if len(content) > 10 * 1024 * 1024:
            return render_template('stats.html', error='Файл слишком большой'), 413
        
        
        stats_result = use_cases.stats(content)
        
        return render_template('stats.html', stats=stats_result)
    
    except Exception as e:
        return render_template('stats.html', error=f'Ошибка обработки файла: {str(e)}'), 500

@app.get('/top')
def top_words_page():
    return render_template('topwords.html')

@app.post('/top')
def top_words_upload():
    try:
        
        if 'file' not in request.files:
            return render_template('topwords.html', error='Пожалуйста, выберите файл'), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('topwords.html', error='Пожалуйста, выберите файл'), 400
        
        if not allowed_file(file.filename):
            return render_template('topwords.html', error='Допускаются только текстовые файлы (.txt)'), 400
        
        
        content = file.read().decode('utf-8', errors='ignore')
        
        
        if len(content) > 10 * 1024 * 1024:
            return render_template('topwords.html', error='Файл слишком большой'), 413
        
        
        normalize_mode = request.form.get('normalize_mode', 'stemming')
        
        
        all_top_words = use_cases.top_words(content, normalize_mode=normalize_mode)
        top_words_list = all_top_words[:20]
        
        return render_template('topwords.html', top_words=top_words_list)
    
    except Exception as e:
        return render_template('topwords.html', error=f'Ошибка обработки файла: {str(e)}'), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('error.html', error='Файл слишком большой'), 413
