from typing import Literal
from ..core.preprocess import filter_stopwords, clean_words
from ..core.tokenize import tokenize_text

# Импорт для лемматизации
from pymystem3 import Mystem

# Создаём объект Mystem один раз (для производительности)
mystem = Mystem()


def _count_words(words: list[str]) -> dict[str, int]:
    """Подсчет количества вхождений слов."""
    counter = {}
    for word in words:
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1
    return counter


def _sort_by_count(item: tuple[str, int]) -> int:
    """Сортирует по количеству вхождений, от большего к меньшему."""
    return -item[1]


def _simple_stem(word: str) -> str:
    """Простой стемминг для русских и английских слов (запасной вариант)."""
    word = word.lower()
    
    if len(word) <= 4:
        return word
    
    # Русские окончания
    russian_endings = [
        'ая', 'яя', 'ое', 'ее', 'ые', 'ие',
        'ого', 'его', 'ому', 'ему', 'ым', 'им',
        'ом', 'ем', 'ой', 'ей',
        'ую', 'юю', 'аю', 'яю',
        'ть', 'ти', 'чь',
        'ет', 'ит', 'ат', 'ят',
        'ут', 'ют', 'ают', 'яют',
        'ал', 'ял', 'ил', 'ол', 'ул',
        'ен', 'ён', 'ян',
        'ок', 'ёк', 'ек',
        'ск', 'нн',
        'ей', 'ий', 'ый', 'ой',
        'а', 'я', 'о', 'е', 'у', 'ю', 'ы', 'и', 'ь', 'ъ'
    ]
    
    for ending in russian_endings:
        if word.endswith(ending):
            result = word[:-len(ending)]
            if len(result) >= 3:
                return result
    
    return word


def _lemmatize_words(words: list[str]) -> list[str]:
    """Лемматизация списка слов с помощью Mystem."""
    if not words:
        return []
    
    # Объединяем слова в строку
    text = ' '.join(words)
    
    # Получаем леммы
    lemmas = mystem.lemmatize(text)
    
    # Фильтруем: убираем пустые строки и знаки пунктуации
    result = []
    for lemma in lemmas:
        lemma = lemma.strip()
        # Оставляем только слова (буквы) длиной больше 1
        if lemma and lemma.isalpha() and len(lemma) > 1:
            result.append(lemma.lower())
    
    return result


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
    
    # Нормализация (стемминг или лемматизация)
    if normalize_mode == "stemming":
        words_normalized = [_simple_stem(word) for word in words_after_filter]
    else:  # lemmatization
        words_normalized = _lemmatize_words(words_after_filter)
    
    # Фильтруем слишком короткие слова
    words_normalized = [word for word in words_normalized if len(word) > 2]
    
    word_counts = _count_words(words_normalized)
    
    return sorted(word_counts.items(), key=_sort_by_count)