from typing import TypedDict, Iterable


class QuantityPercent(TypedDict):
    quantity: int
    percent: float


class SymbolStats(TypedDict):
    alphas: QuantityPercent
    digits: QuantityPercent
    spaces: QuantityPercent
    punctuation: QuantityPercent


class TokensStats(TypedDict):
    paragraphs: int
    sentences: int
    words: int


class TextStats(TypedDict):
    tokens: TokensStats
    symbols: SymbolStats


class SearchResult(TypedDict):
    result: str
    start: int
    end: int


class Tokens(TypedDict):
    paragraphs: list[str]
    sentences: list[str]
    words: list[str]
