from wordcloud import WordCloud
import io
import base64
from ..core.preprocess import clean_text

def execute(text: str, mode: str = "base"):
    data = clean_text(text) if mode == "full" else text
    
    wc = WordCloud(width=800, height=400, background_color='white').generate(data)   #генерация клаудвордс
    
    img = io.BytesIO()
    wc.to_image().save(img, format='PNG')   #сохраняем
    img.seek(0)
    
    return base64.b64encode(img.getvalue()).decode()
