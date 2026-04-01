import re
from .types import Tokens

def _get_words(text: str) -> list[str]:
    return re.findall(r'[а-яёА-ЯЁa-zA-Z]+', text)

def _get_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r'\n+', text) if p.strip()]

def _get_sentences(text: str) -> list[str]:
    sentences = re.split(r'(?<=[.!?])[\s\n]+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def tokenize_text(text: str) -> Tokens:
    if not text:
        return {"paragraphs": [], "sentences": [], "words": []}
    return {
        "paragraphs": _get_paragraphs(text),
        "sentences": _get_sentences(text),
        "words": _get_words(text),
    }