import re
from .types import Tokens

def _get_words(text: str) -> list[str]:
    return re.findall('[а-яёА-ЯЁa-zA-Z]+', text)

def _get_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r'\n+', text) if p.strip()]

def _get_sentences(text: str) -> list[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]


def tokenize_text(text: str) -> Tokens:
    return {
        "paragraphs": _get_paragraphs(text),
        "sentences": _get_sentences(text),
        "words": _get_words(text),
    }
