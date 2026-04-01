import re
import pathlib

from ..core.types import TextStats, SymbolStats, Tokens, TokensStats


def stats(text: str, pos: bool = False) -> TextStats:
    """Функция для подсчета статистик.

    Args:
        text: текст для расчета статистик
        pos: опция, добавляет аналитику по частям речи

    Returns:
        Статистика, сгруппированная по токенам, символам и,
        опционально, морфологическим характеристикам

        Например, для строки `\tПроверка!\nНовая строка` это
        будет:
        {
            "tokens": {
                "paragraphs": 2,
                "sentences": 2,
                "words": 3,
            },
            "symbols": {
                "alphas": {
                    "quantity": 19,
                    "percent": 82.61
                },
                "digits": {
                    "quantity": 0,
                    "percent": 0.00
                },
                "spaces": {
                    "quantity": 3,
                    "percent": 13.04
                },
                "punctuation": {
                    "quantity": 1,
                    "percent": 4.35
                }
            }
        }

    """

    return {"tokens": _get_tokens_stats(text), "symbols": _get_symbols_stats(text)}


def _get_symbols_stats(text: str) -> SymbolStats:
    """Посимвольная статистика (количество и процент)."""
    import string

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
        elif symbol in string.punctuation:
            count_punctuation += 1

    total = len(text) if len(text) > 0 else 1
    return {
        "alphas": {"quantity": count_alphas, "percent": round(count_alphas / total * 100, 2)},
        "digits": {"quantity": count_digits, "percent": round(count_digits / total * 100, 2)},
        "spaces": {"quantity": count_spaces, "percent": round(count_spaces / total * 100, 2)},
        "punctuation": {"quantity": count_punctuation, "percent": round(count_punctuation / total * 100, 2)},
    }


def _get_tokens_stats(text: str) -> TokensStats:
    """Подсчет количества токенов."""
    from ..core.tokenize import tokenize_text
    
    tokens = tokenize_text(text)
    return {
        "paragraphs": len(tokens["paragraphs"]),
        "sentences": len(tokens["sentences"]),
        "words": len(tokens["words"])
    }


def _get_pos_stats(text: str):
    """Подсчет pos-аналитики"""

    return
