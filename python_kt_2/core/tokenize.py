import re
from .types import Tokens

def _get_words(text: str) -> list[str]:
    """Разбиение на слова (без обработки)
    """
    return re.split(r'\s+', text)


def _get_paragraphs(text: str) -> list[str]:
    """Разбиение на параграфы (абзацы)"""
    return [p.strip() for p in text.split('\n\n') if p.strip()]


def _get_sentences(text: str) -> list[str]:
    """Разбиение на предложения"""
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def tokenize_text(text: str) -> Tokens:
    """Разбиение текста на токены.

    Разбиение текста на токены:
    - параграфы (абзацы),
    - предложения,
    - слова
    """
    return {
        "paragraphs": _get_paragraphs(text),
        "sentences": _get_sentences(text),
        "words": _get_words(text),
    }
