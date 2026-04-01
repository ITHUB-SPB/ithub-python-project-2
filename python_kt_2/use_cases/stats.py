import re
import pathlib

from ..core.types import TextStats, SymbolStats, Tokens, TokensStats


def stats(text: str, pos: bool = False) -> TextStats:
    result = {
        "tokens": _get_tokens_stats(text),
        "symbols": _get_symbols_stats(text),
    }
    
    if pos:
        result["pos_stats"] = _get_pos_stats(text)
    
    return result



def _get_symbols_stats(text: str) -> SymbolStats:
    if not text:
        return {
            "alphas": {"quantity": 0, "percent": 0.0},
            "digits": {"quantity": 0, "percent": 0.0},
            "spaces": {"quantity": 0, "percent": 0.0},
            "punctuation": {"quantity": 0, "percent": 0.0},
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

    total = len(text)

    return {
        "alphas": {
            "quantity": count_alphas,
            "percent": round(count_alphas / total * 100, 2)
        },
        "digits": {
            "quantity": count_digits,
            "percent": round(count_digits / total * 100, 2)
        },
        "spaces": {
            "quantity": count_spaces,
            "percent": round(count_spaces / total * 100, 2)
        },
        "punctuation": {
            "quantity": count_punctuation,
            "percent": round(count_punctuation / total * 100, 2)
        },
    }



def _get_tokens_stats(text: str) -> TokensStats:
   
    text = text.strip()

    paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = [p for p in paragraphs if p.strip()]
    sentences = re.split(r'[.!?…]+', text)
    sentences = [s for s in sentences if s.strip()]

    words = re.findall(r'[а-яА-ЯёЁa-zA-Z]+', text)

    return {
        "paragraphs": len(paragraphs),
        "sentences": len(sentences),
        "words": len(words),
    }


def _get_pos_stats(text: str):
    words = re.findall(r'[а-яА-ЯёЁ]+', text.lower())
    pos_counter = Сounter()
    
    for word in words:
        if word.endswith(('ть', 'ти', 'тся', 'ться', 'ил', 'ала', 'ало', 'али')):
            pos_counter['VERB'] += 1
        elif word.endswith(('ый', 'ий', 'ая', 'яя', 'ое', 'ее', 'ые', 'ие')):
            pos_counter['ADJF'] += 1
        elif word.endswith(('о', 'е', 'ом', 'ем', 'ой', 'ей')):
            pos_counter['ADVB'] += 1
        elif word in ('я', 'ты', 'он', 'она', 'оно', 'мы', 'вы', 'они'):
            pos_counter['NPRO'] += 1
        elif word.isdigit() or word in ('один', 'два', 'три', 'четыре', 'пять'):
            pos_counter['NUMR'] += 1
        else:
            pos_counter['NOUN'] += 1
    
    return dict(pos_counter.most_common())
