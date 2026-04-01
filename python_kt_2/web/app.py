from pathlib import Path
from flask import Flask, render_template, request
from ..use_cases.stats import stats as calculate_stats
from ..use_cases.top_words import top_words as get_top_words

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = BASE_DIR / 'corpus'


def get_corpus_files():
    if CORPUS_DIR.exists():
        return [f.name for f in CORPUS_DIR.iterdir() if f.is_file()]
    return []
@app.get('/')
def index():
    return render_template('index.html')


@app.route('/stats', methods=['GET', 'POST'])
def stats():
    files = get_corpus_files()
    selected_file = None
    stats_data = None
    pos_data = None
    error = None

    if request.method == 'POST':
        selected_file = request.form.get('filename')
        file_path = CORPUS_DIR / selected_file if selected_file else None

        if not selected_file or not file_path.exists():
            error = "Файл не найден."
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                full_results = calculate_stats(text, pos=True)
                stats_data = full_results.get("symbols")
            except Exception as e:
                error = f"Ошибка: {e}"

    return render_template(
        'stats.html',
        files=files,
        selected_file=selected_file,
        stats=stats_data,
        pos_stats=pos_data,
        error=error
    )

@app.route('/top_words', methods=['GET', 'POST'])
def top_words():
    files = get_corpus_files()
    selected_file = None
    words_data = None
    error = None

    if request.method == 'POST':
        selected_file = request.form.get('filename')
        limit = request.form.get('limit', 10, type=int)
        file_path = CORPUS_DIR / selected_file if selected_file else None

        if not selected_file or not file_path.exists():
            error = "Файл не найден."
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                words_data = get_top_words(text, top_n_words=limit)
            except Exception as e:
                error = f"Ошибка при анализе слов: {e}"

    return render_template(
        'topwords.html',
        files=files,
        selected_file=selected_file,
        words=words_data,
        error=error
    )