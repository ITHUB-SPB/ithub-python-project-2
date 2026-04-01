from typing import Literal
from collections import Counter
from ..core.preprocess import filter_stopwords, clean_words, stem_words, lemmatize_words

def _count_words(words: list[str]) -> dict[str, int]:
    """Подсчет количества вхождений слов."""
    return dict(Counter(words))

def _sort_by_count(item: tuple[str, int]) -> tuple[int, str]:
    """Сортирует по количеству (от большего к меньшему),
    затем по алфавиту (по возрастанию).
    """
    return (-item[1], item[0])

def top_words(
    text: str, 
    normalize_mode: Literal["stemming", "lemmatization"] = "stemming",
    limit: int = 20
) -> list[tuple[str, int]]:
    """Подсчет топ важных слов."""
    
    # Приводим к нижнему регистру и разбиваем на слова
    initial_words = text.lower().split()
    
    # Очистка от знаков пунктуации по краям
    words_after_clean = clean_words(initial_words)
    
    # фильтрация стоп-слов
    words_after_filter = filter_stopwords(words_after_clean)
    
    # нормализация (выбор режима)
    if normalize_mode == "stemming":
        normalized_words = stem_words(words_after_filter)
    elif normalize_mode == "lemmatization":
        normalized_words = lemmatize_words(words_after_filter)
    else:
        normalized_words = words_after_filter
        
    # подсчет и сортировка
    counted = _count_words(normalized_words)
    sorted_items = sorted(counted.items(), key=_sort_by_count)
    
    return sorted_items[:limit]