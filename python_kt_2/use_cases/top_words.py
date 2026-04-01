from typing import Literal
from ..core.preprocess import filter_stopwords, clean_words
from python_kt_2.core.tokenize import tokenize_text


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
    
    
    
    initial_words = tokenize_text(text)["words"]
    words_after_clean = clean_words(initial_words)
    words_after_filter = filter_stopwords(words_after_clean)
    
    return sorted(_count_words(words_after_filter).items(), key=_sort_by_count)
    