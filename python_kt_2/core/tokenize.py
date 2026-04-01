import re
from .types import Tokens

def _get_words(text: str) -> list[str]:
    paragraphs = re.split(r'\n\s*\n', text.strip())
    return [p.strip() for p in paragraphs if p.strip()]


def tokenize_text(text: str) -> Tokens:
    sentence_endings = r'(?<=[.!?…])\s+(?=[А-ЯЁA-Z])|(?<=[.!?…])\s*$'
    sentences = re.split(sentence_endings, text.strip())
    return [s.strip() for s in sentences if s.strip()]

def _get_words(text: str) -> list[str]:
    return re.findall(r"[а-яА-ЯёЁa-zA-Z]+", text)

def tokenize_text(text: str) -> Tokens:
    return {
        "paragraphs": (text),
        "sentences": (text),
        "words": _get_words(text),
    }