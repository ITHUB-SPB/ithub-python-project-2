import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template,request
from use_cases.stats import get_symbols_stats
from use_cases.word_cloud import word_cloud 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    corpus_dir = Path(__file__).parent.parent / "corpus"
    files = []
    if corpus_dir.exists():
        files = [f.name for f in corpus_dir.iterdir() if f.is_file() and f.suffix == '.txt']
    
    if request.method == 'GET':
        return render_template('stats.html', files=files)
    
    filename = request.form.get('filename', '')
    
    if not filename:
        return render_template('stats.html', error="выберите файл", files=files)
    
    filepath = corpus_dir / filename
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        return render_template('stats.html', error=f"ошибка чтения: {str(e)}", files=files)
    
    stats = get_symbols_stats(text)
    return render_template('stats.html', 
                         stats=stats, 
                         files=files, 
                         selected_file=filename)
    
@app.route('/cloud', methods=['GET', 'POST'])
def cloud():
    corpus_dir = Path(__file__).parent.parent / "corpus"
    files = []
    if corpus_dir.exists():
        files = [f.name for f in corpus_dir.iterdir() if f.is_file() and f.suffix == '.txt']
    
    if request.method == 'POST':
        filename = request.form.get('filename', '')
        preprocess_mode = request.form.get('preprocess_mode', 'basic')
        
        if not filename:
            return render_template('cloud.html', error="Выберите файл", files=files)
        
        filepath = corpus_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            img_base64 = word_cloud(text, preprocess_mode)
            return render_template('cloud.html', 
                                 wordcloud_img=img_base64, 
                                 mode=preprocess_mode,
                                 selected_file=filename,
                                 files=files)
        except Exception as e:
            return render_template('cloud.html', 
                                 error=f"ошибка: {str(e)}", 
                                 files=files,
                                 selected_file=filename)
    
    return render_template('cloud.html', files=files)

if __name__ == "__main__":
    app.run(debug=True)