import pathlib
from typing import Set
from string import punctuation, whitespace


def _load_stopwords() -> Set[str]:
    """Загрузка стоп-слов из файла."""
    path_to_file = pathlib.Path(__file__).parent / "stopwords.txt"
    with open(path_to_file, encoding="utf-8") as f:
        return set(f.read().splitlines())


def filter_stopwords(words: list[str]) -> list[str]:
    """Фильтрация стоп-слов."""
    stopwords_lower = _load_stopwords()
    print(f"Загружено стоп-слов: {len(stopwords_lower)}")
    print(f"Пример стоп-слов: {list(stopwords_lower)[:10]}")

    stopwords_title = set(stopword.title() for stopword in stopwords_lower)
    stopwords_upper = set(stopword.upper() for stopword in stopwords_lower)

    all_stopwords = stopwords_lower | stopwords_title | stopwords_upper

    return [
        word for word in words
        if word and word not in all_stopwords
    ]


def clean_words(words: list[str]) -> list[str]:
    """Очистка слов от пунктуации."""
    cleaned_words = []
    for word in words:
        clean_word = word.strip(punctuation + whitespace + "—«»…")
        if clean_word:
            cleaned_words.append(clean_word)
    return cleaned_words