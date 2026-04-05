from typing import Literal
from ..core.preprocess import filter_stopwords, clean_words
from ..core.tokenize import tokenize_text


def _count_words(words: list[str]) -> dict[str, int]:
    counter = {}
    for word in words:
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1
    return counter


def _sort_by_count(item: tuple[str, int]) -> int:
    return -item[1]


def top_words(
    text: str, 
    normalize_mode: Literal["stemming", "lemmatization"] = "stemming", 
) -> list[tuple[str, int]]:
    """Подсчет топ-N-важных слов.

    Получает текст, разбивает на слова, убирает пунктуацию и пробельные символы,
    фильтрует стоп-слова, нормализует (либо стемминг, либо лемматизация),
    подсчитывает и возвращает список кортежей для топ-N-важных слов.
    """
    
    initial_words = tokenize_text(text)["words"]
    
    words_after_clean = clean_words(initial_words)
    
    words_after_filter = filter_stopwords(words_after_clean)
    
    if normalize_mode == "stemming":
        # Стемминг
        from nltk.stem import SnowballStemmer
        stemmer = SnowballStemmer("russian")
        words_normalized = [stemmer.stem(word) for word in words_after_filter]
    else:
        from pymystem3 import Mystem
        mystem = Mystem()
        text_for_lemmatize = ' '.join(words_after_filter)
        lemmas = mystem.lemmatize(text_for_lemmatize)
        words_normalized = [lemma for lemma in lemmas if lemma.strip()]
    
    word_counts = _count_words(words_normalized)
    
    return sorted(word_counts.items(), key=_sort_by_count)