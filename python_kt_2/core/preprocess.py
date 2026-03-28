import pathlib
from string import punctuation, whitespace
from typing import Iterable, Set


def _load_stopwords() -> Set[str]:
    path_to_file = pathlib.Path() / "src" / "python_kt_2" / "core" / "stopwords.txt"
    with open(path_to_file, encoding="utf-8") as f:
        return set(f.read().splitlines())


def filter_stopwords(words: list[str]) -> list[str]:
    stopwords_lower = _load_stopwords()
    stopwords_title = set(stopword.title() for stopword in stopwords_lower)

    # TODO дописать фильтрацию стоп-слов

    return [word for word in words if word]


def clean_words(words: list[str]) -> list[str]:
    return [word.strip(punctuation + whitespace + "—«»…") for word in words]


def preprocess_text(text: str) -> Iterable[str]:
    """
    Предобработка текста:
    - токенизация по словам
    - фильтр по стоп-словам
    - очистка от знаков препинания.
    Returns:
        Список слов, используемых в тексте
    """
    words = tokenize_text_by_words(text)

    for index in range(len(words)):
        words[index] = words[index].strip(punctuation + whitespace + "—«»")

    with open(
        pathlib.Path() / "python_kt_2" / "core" / "stopwords.txt", encoding="utf-8"
    ) as f:
        stop_words = f.read().splitlines()

    words = [w.upper() for w in words if w and not w.lower() in stop_words]
    return words


def tokenize_text_by_words(text: str) -> Iterable[str]:
    """
    Разбиение текста на слова.
    """
    text = text.replace("\n", " ").replace("\r\n", " ")
    words = text.split(" ")
    return words
