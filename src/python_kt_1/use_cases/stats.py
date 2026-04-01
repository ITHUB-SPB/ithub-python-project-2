import re
from ..core.types import TextStats, SymbolStats, Tokens, TokensStats

def stats(text: str, pos: bool = False) -> TextStats:
    return {"tokens": _get_tokens_stats(text), "symbols": _get_symbols_stats(text)}

def _get_symbols_stats(text: str) -> SymbolStats:
    """Посимвольная статистика (количество и процент)."""
    total_chars = len(text)

    if total_chars == 0:
        return {
            "alphas": {"quantity": 0, "percent": 0.0},
            "digits": {"quantity": 0, "percent": 0.0},
            "spaces": {"quantity": 0, "percent": 0.0},
            "punctuation": {"quantity": 0, "percent": 0.0}
        }

    count_alphas = 0
    count_digits = 0
    count_spaces = 0
    count_punctuation = 0

    for symbol in text:
        if symbol.isalpha():
            count_alphas += 1
        elif symbol.isdigit():
            count_digits += 1
        elif symbol.isspace():
            count_spaces += 1
        else:
            count_punctuation += 1

    return {
        "alphas": {"quantity": count_alphas, "percent": round((count_alphas / total_chars) * 100, 2)},
        "digits": {"quantity": count_digits, "percent": round((count_digits / total_chars) * 100, 2)},
        "spaces": {"quantity": count_spaces, "percent": round((count_spaces / total_chars) * 100, 2)},
        "punctuation": {"quantity": count_punctuation, "percent": round((count_punctuation / total_chars) * 100, 2)}
    }


def _get_tokens_stats(text: str) -> TokensStats:
    text = text.strip()
    return {
        "paragraphs": len(text.splitlines()),
        "sentences": len(re.split(r"[.!?]\s+", text)),
        "words": len(re.split(r"\s+", text)),
    }

def _get_pos_stats(text: str):
    """Подсчет pos-аналитики"""
    return