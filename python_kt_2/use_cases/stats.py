from ..core.preprocess import get_basic_stats

def execute(text: str, pos_enabled: bool = False):
    stats = get_basic_stats(text)
    if pos_enabled:
        stats["pos_info"] = "POS-теггинг активирован (в режиме ожидания)"
    return stats