from typing import Literal
from wordcloud import WordCloud
from ..core.preprocess import filter_stopwords


def word_cloud(
        text: str,
        preprocess_mode: Literal["basic", "full"] = "basic"
):
    """Построение облака важных слов.

    Получает текст, выполняет базовую предобработку (разбивает на слова, 
    убирает пунктуацию и пробельные символы, фильтрует стоп-слова. 

    В режиме полной предобработки проводит стемминг либо лемматизацию.

    Возможности:
    - сохранение результата (изображения) в файл
    - два уровня предобработки (базовый, полный).
    """

    if preprocess_mode == "basic":
        return WordCloud().generate(text).to_file()

    return