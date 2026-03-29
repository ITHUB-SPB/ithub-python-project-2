import re
from .types import Tokens
import pymorphy3
morph = pymorphy3.MorphAnalyzer()

def _get_words(text: str) -> list[str]:
    """Разбиение на слова (без обработки)"""
    return re.findall(r"[а-яёА-ЯЁa-zA-Z]+", text)

def lemmatize_word(word: str) -> str:

    return morph.parse(word.lower())[0].normal_form


def stem_word(word: str) -> str:

    word = word.lower()

    suffixes = ['ing', 'ed', 'ly', 'es', 's']
    for suffix in suffixes:
        if word.endswith(suffix):
            return word[:-len(suffix)]
    return word


def normalize_word(word: str, method: str) -> str:
    if method == 'stemming':
        return stem_word(word)
    elif method == 'lemmatization':
        return lemmatize_word(word)
    return word.lower()  

def _get_paragraphs(text: str) -> list[str]:
    return [p for p in text.split('\n') if p.strip()]

def _get_sentences(text: str) -> list[str]:
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

def tokenize_text(text: str) -> Tokens:
    """Разбиение текста на токены.

    Разбиение текста на токены:
    - параграфы (абзацы),
    - предложения,
    - слова
    """

    # TODO допишите функции _get_paragraphs, _get_sentences

    return {
        "paragraphs": _get_paragraphs(text),
        "sentences": _get_sentences(text),
        "words": _get_words(text),
    }


