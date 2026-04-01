from typing import Literal
from ..core.preprocess import filter_stopwords, clean_words
from python_kt_2.core.tokenize import tokenize_text
import pymorphy3
from nltk.stem import SnowballStemmer

morph = pymorphy3.MorphAnalyzer()
stemmer = SnowballStemmer("russian")


def _count_words(words: list[str]) -> dict[str, int]:
    counter = {}

    for word in words:
        word = word.lower()
        counter[word] = counter.get(word, 0) + 1
    return counter


def _sort_by_count(item: tuple[str, int]) -> int:
    return -item[1]


def top_words(
        text: str,
        normalize_mode: Literal["stemming", "lemmatization"] = "stemming",
        top_n_words: int = 10,
) -> list[tuple[str, int]]:

    initial_words = tokenize_text(text)["words"]
    words_after_clean = clean_words(initial_words)
    words_after_filter = filter_stopwords(words_after_clean)

    normalized_words = []
    for word in words_after_filter:
        if normalize_mode == "lemmatization":
            normalized_words.append(morph.parse(word)[0].normal_form)
        else:
            normalized_words.append(stemmer.stem(word))

    word_counts = _count_words(normalized_words)
    sorted_top = sorted(word_counts.items(), key=_sort_by_count)

    return sorted_top[:top_n_words]
