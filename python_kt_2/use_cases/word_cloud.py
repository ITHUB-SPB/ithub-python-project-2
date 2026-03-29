from typing import Literal
from wordcloud import WordCloud
import base64
import io
from collections import Counter
from core.tokenize import tokenize_text, normalize_word
from core.preprocess import filter_stopwords, clean_words

def word_cloud(
    text: str, 
    preprocess_mode: Literal["basic", "stemming", "lemmatization"] = "stemming" 
):
    """Построение облака важных слов.

    Получает текст, выполняет базовую предобработку (разбивает на слова, 
    убирает пунктуацию и пробельные символы, фильтрует стоп-слова. 

    При указании режима предобработки, отличного от базового, нормализует 
    (стеммингом либо лемматизацией). 

    Возможности:
    - сохранение результата (изображения) в файл
    - три уровня предобработки (базовый, стемминг, лемматизация).
    """
    tokens = tokenize_text(text)

    words = tokens["words"]  
    words = clean_words(words)
    words = [w for w in words if w]

    if preprocess_mode != "basic":
        words = [normalize_word(w, preprocess_mode) for w in words]

    words = filter_stopwords(words)

    word_freq = Counter(words)

    wc = WordCloud(
        width=800,
        height=400,
        background_color='white',
        max_words=10000,
        colormap='viridis'
    )
    wc.generate_from_frequencies(word_freq)

    img_buffer = io.BytesIO()
    wc.to_image().save(img_buffer, format='PNG')
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

    return img_base64