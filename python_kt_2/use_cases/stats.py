import re
from ..core.types import TextStats, SymbolStats, TokensStats

def stats(text: str, pos: bool = False) -> TextStats:
    if not text:
        return {"tokens": _get_tokens_stats(""), "symbols": _get_symbols_stats("")}
    return {"tokens": _get_tokens_stats(text), "symbols": _get_symbols_stats(text)}

def _get_symbols_stats(text: str) -> SymbolStats:
    total = len(text) or 1
    counts = {
        "alphas": 0,
        "digits": 0,
        "spaces": 0,
        "punctuation": 0
    }

    for symbol in text:
        if symbol.isalpha():
            counts["alphas"] += 1
        elif symbol.isdigit():
            counts["digits"] += 1
        elif symbol.isspace():
            counts["spaces"] += 1
        else:
            counts["punctuation"] += 1

    return {
        k: {"quantity": v, "percent": round((v / total) * 100, 2)}
        for k, v in counts.items()
    }

def _get_tokens_stats(text: str) -> TokensStats:
    if not text.strip():
        return {"paragraphs": 0, "sentences": 0, "words": 0}

    paragraphs = len([p for p in text.split('\n') if p.strip()])
    sentences = len(re.findall(r'[.!?]+', text))
    words = len(text.split())

    return {
        "paragraphs": paragraphs,
        "sentences": max(sentences, 1) if text.strip() else 0,
        "words": words
    }