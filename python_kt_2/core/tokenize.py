import re
from .types import Tokens

def _get_paragraphs(text: str) -> list[str]:
    """Разбиение текста на абзацы.
    Абзацем считается текст, разделенный одним или несколькими переносами строк.
    """
    return [p.strip() for p in re.split(r'\n+', text) if p.strip()]


def _get_sentences(text: str) -> list[str]:
    """Разбиение текста на предложения.
    Используется регулярное выражение, которое ищет знаки завершения (. ! ?)
    """

    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def _get_words(text: str) -> list[str]:
    """Разбиение на слова.
    Находит все последовательности буквенно-цифровых символов.
    """
    return re.findall(r'\w+', text)


def tokenize_text(text: str) -> Tokens:
    """Разбиение текста на токены: параграфы, предложения, слова."""
    clean_text = text.strip()

    if not clean_text:
        return {
            "paragraphs": [],
            "sentences": [],
            "words": [],
        }

    return {
        "paragraphs": _get_paragraphs(clean_text),
        "sentences": _get_sentences(clean_text),
        "words": _get_words(clean_text),
    }

