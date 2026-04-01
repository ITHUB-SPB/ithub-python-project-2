import re

def clean_text(text: str) -> str:
    """Очистка текста от лишних символов."""
    text = text.lower()
    # Удаляем всё, кроме букв и пробелов
    text = re.sub(r'[^а-яёa-z\s]', '', text)
    return text

def get_basic_stats(text: str) -> dict:
    """Подсчет базовых метрик текста."""
    words = [w for w in text.split() if w]
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    
    return {
        "total_words": len(words),
        "unique_words": len(set(word.lower() for word in words)),
        "total_sentences": len(sentences)
    }