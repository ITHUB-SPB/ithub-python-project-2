import re
from .types import Tokens

def _get_paragraphs(text: str) -> list[str]:
    """Разбиение текста на абзацы."""
    return [p for p in re.split(r'\n\s*\n', text.strip()) if p]

def _get_sentences(paragraph: str) -> list[str]:
    """Разбиение абзаца на предложения."""
    return re.split(r'(?<=[.!?])\s+', paragraph.strip())

def _get_words(text: str) -> list[str]:
    """Разбиение на слова (без обработки)."""
    return re.findall(r"[\w'-]+", text)

def tokenize_text(text: str) -> Tokens:
    """Разбиение текста на токены."""
    paragraphs = _get_paragraphs(text)
    sentences = []
    for p in paragraphs:
        sentences.extend(_get_sentences(p))
    words = _get_words(text)
    
    return {
        "paragraphs": paragraphs,
        "sentences": sentences,
        "words": words,
    }